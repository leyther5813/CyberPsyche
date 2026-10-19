import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session as DBSession
from fastapi import HTTPException, status

from app.models.user import User, Consent, DigitalContext
from app.models.scenario import Scenario, EvidenceItem
from app.models.session import Session, SessionScenario
from app.models.behaviour import BehaviourEvent, Decision, ScenarioOutcome
from app.models.intervention import InterventionDelivery
from app.models.resilience_profile import ResilienceProfile

from app.schemas.scenario_schema import (
    ScrubbedNextScenarioResponse, EvidenceItemScrubbed, EvidenceItemRevealed
)
from app.schemas.session_schema import DecisionSubmissionDTO, DecisionOutcomeResponseDTO
from app.schemas.event_schema import BehaviourEventDTO

from app.scoring.constructs import (
    calculate_decision_quality, calculate_under_caution,
    calculate_over_caution, calculate_independent_verification,
    calculate_evidence_depth, calculate_reason_alignment
)
from app.scoring.sdt import calculate_sdt_metrics
from app.intervention.selector import select_targeted_intervention

PHASE_ORDER = ["consent", "onboarding", "baseline", "intervention", "retest", "transfer", "profile"]

def create_session(db: DBSession, user_id: str, arm: str = "targeted", form_assignment: str = "Form_A") -> Session:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    consent = db.query(Consent).filter(Consent.user_id == user_id).first()
    if not consent:
        raise HTTPException(status_code=400, detail="Consent is required before creating a study session")

    # Fetch available scenarios from DB with explicit family_id ordering for cross-database determinism
    baseline_scenarios = db.query(Scenario).filter(Scenario.phase_pool == "baseline").order_by(Scenario.family_id).all()
    retest_scenarios = db.query(Scenario).filter(Scenario.phase_pool == "retest").order_by(Scenario.family_id).all()
    transfer_scenarios = db.query(Scenario).filter(Scenario.phase_pool == "transfer").order_by(Scenario.family_id).all()

    if not baseline_scenarios or not retest_scenarios or not transfer_scenarios:
        raise HTTPException(status_code=500, detail="Scenario set is not seeded in database")

    # Form_A selects first 6 families (0:6), Form_B selects offset 6 families (4:10)
    if form_assignment == "Form_B":
        b_selected = (baseline_scenarios * 2)[4:10]
        r_selected = (retest_scenarios * 2)[4:10]
        t_selected = (transfer_scenarios * 2)[4:10]
    else:
        b_selected = baseline_scenarios[:6]
        r_selected = retest_scenarios[:6]
        t_selected = transfer_scenarios[:6]

    session = Session(
        id=str(uuid.uuid4()),
        user_id=user_id,
        arm=arm,
        form_assignment=form_assignment,
        current_phase="baseline",
        started_at=datetime.now(timezone.utc),
        scenario_set_version="scenario_set_v1"
    )
    db.add(session)
    db.flush()

    order_idx = 0
    for sc in b_selected:
        db.add(SessionScenario(id=str(uuid.uuid4()), session_id=session.id, scenario_id=sc.id, phase="baseline", order_idx=order_idx))
        order_idx += 1

    for sc in r_selected:
        db.add(SessionScenario(id=str(uuid.uuid4()), session_id=session.id, scenario_id=sc.id, phase="retest", order_idx=order_idx))
        order_idx += 1

    for sc in t_selected:
        db.add(SessionScenario(id=str(uuid.uuid4()), session_id=session.id, scenario_id=sc.id, phase="transfer", order_idx=order_idx))
        order_idx += 1

    db.commit()
    db.refresh(session)
    return session

def get_next_scenario(db: DBSession, session_id: str, user_id: str) -> Dict[str, Any]:
    session = db.query(Session).filter(Session.id == session_id, Session.user_id == user_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    current_phase = session.current_phase

    if current_phase not in ["baseline", "retest", "transfer"]:
        return {
            "session_id": session.id,
            "status": "phase_transition",
            "current_phase": current_phase,
            "message": f"Session is in {current_phase} phase."
        }

    # Find scenarios for current phase
    phase_scenarios = (
        db.query(SessionScenario)
        .filter(SessionScenario.session_id == session_id, SessionScenario.phase == current_phase)
        .order_by(SessionScenario.order_idx)
        .all()
    )

    # Find which ones have already been decided
    decided_scenario_ids = set(
        d.scenario_id for d in db.query(Decision.scenario_id).filter(Decision.session_id == session_id).all()
    )

    next_ss = None
    for ss in phase_scenarios:
        if ss.scenario_id not in decided_scenario_ids:
            next_ss = ss
            break

    if not next_ss:
        # Current phase completed! Transition state machine
        if current_phase == "baseline":
            session.current_phase = "intervention"
        elif current_phase == "retest":
            session.current_phase = "transfer"
        elif current_phase == "transfer":
            session.current_phase = "profile"
            session.completed_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(session)
        
        return {
            "session_id": session.id,
            "status": "phase_completed",
            "current_phase": session.current_phase,
            "message": f"Completed {current_phase} phase. Transitioned to {session.current_phase}."
        }

    # Fetch scenario from DB
    sc = db.query(Scenario).filter(Scenario.id == next_ss.scenario_id).first()
    if not sc:
        raise HTTPException(status_code=404, detail="Scenario record missing in database")

    # CRITICAL RESEARCH INTEGRITY RULE:
    # Scrub ground truth, evidence signals, diagnosticity, official_channel flags, and action safety classifications!
    payload = sc.json_payload
    available_evidence = [
        EvidenceItemScrubbed(id=e["id"], label=e["label"])
        for e in payload.get("evidence", [])
    ]

    scrubbed_response = ScrubbedNextScenarioResponse(
        session_id=session.id,
        scenario_id=sc.id,
        phase=current_phase,
        context=sc.context,
        channel=sc.channel,
        persona=sc.persona or "",
        pressure=sc.pressure,
        narrative=payload.get("narrative", ""),
        message={
            "sender_display": payload.get("message", {}).get("sender_display", ""),
            "body": payload.get("message", {}).get("body", ""),
            "attachment": payload.get("message", {}).get("attachment", "")
        },
        available_evidence=available_evidence
    )

    # Log 'view' event for telemetry
    event = BehaviourEvent(
        id=str(uuid.uuid4()),
        session_id=session.id,
        scenario_id=sc.id,
        event_type="view",
        payload={"phase": current_phase},
        ts=datetime.now(timezone.utc)
    )
    db.add(event)
    db.commit()

    return scrubbed_response.model_dump()

def log_event(db: DBSession, session_id: str, user_id: str, event_dto: BehaviourEventDTO) -> Dict[str, Any]:
    session = db.query(Session).filter(Session.id == session_id, Session.user_id == user_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # DEFECT 1 FIX: Evidence Gating Validation
    # 1. Verify scenario belongs to participant's current session
    ss_record = (
        db.query(SessionScenario)
        .filter(SessionScenario.session_id == session_id, SessionScenario.scenario_id == event_dto.scenario_id)
        .first()
    )
    if not ss_record:
        raise HTTPException(status_code=400, detail="Scenario does not belong to this session")

    # 2. Verify scenario belongs to current active phase
    if ss_record.phase != session.current_phase:
        raise HTTPException(status_code=400, detail="Cannot log events for a scenario outside the active phase")

    # 3. Verify scenario is currently active and un-decided
    decided = db.query(Decision).filter(Decision.session_id == session_id, Decision.scenario_id == event_dto.scenario_id).first()
    if decided:
        raise HTTPException(status_code=400, detail="Cannot log events or open evidence after decision has been submitted")

    # 4. Verify scenario is the active next scenario in sequence
    phase_scenarios = (
        db.query(SessionScenario)
        .filter(SessionScenario.session_id == session_id, SessionScenario.phase == session.current_phase)
        .order_by(SessionScenario.order_idx)
        .all()
    )
    decided_ids = set(
        d.scenario_id for d in db.query(Decision.scenario_id).filter(Decision.session_id == session_id).all()
    )
    active_scenario_id = None
    for ss in phase_scenarios:
        if ss.scenario_id not in decided_ids:
            active_scenario_id = ss.scenario_id
            break

    if event_dto.scenario_id != active_scenario_id:
        raise HTTPException(status_code=400, detail="Cannot log events for a scenario that is not currently active")

    event = BehaviourEvent(
        id=str(uuid.uuid4()),
        session_id=session.id,
        scenario_id=event_dto.scenario_id,
        event_type=event_dto.event_type,
        payload=event_dto.payload or {},
        ts=datetime.now(timezone.utc)
    )
    db.add(event)
    db.commit()

    # If open_evidence, reveal ONLY id, label, and value for that item (no signal, diagnosticity, or ground truth)
    if event_dto.event_type == "open_evidence" and event_dto.payload and "evidence_id" in event_dto.payload:
        ev_id_raw = event_dto.payload["evidence_id"]
        ev_id = f"{event_dto.scenario_id}-{ev_id_raw}" if not ev_id_raw.startswith(event_dto.scenario_id) else ev_id_raw
        ev_item = db.query(EvidenceItem).filter(EvidenceItem.id == ev_id, EvidenceItem.scenario_id == event_dto.scenario_id).first()
        if ev_item:
            return {
                "event_id": event.id,
                "status": "logged",
                "revealed_evidence": {
                    "id": ev_id_raw,
                    "label": ev_item.label,
                    "value": ev_item.value
                }
            }

    return {"event_id": event.id, "status": "logged"}

def submit_decision(db: DBSession, session_id: str, user_id: str, dto: DecisionSubmissionDTO) -> DecisionOutcomeResponseDTO:
    session = db.query(Session).filter(Session.id == session_id, Session.user_id == user_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.current_phase not in ["baseline", "retest", "transfer"]:
        raise HTTPException(status_code=400, detail=f"Cannot submit decision while session is in {session.current_phase} phase")

    # Check for duplicate decision
    existing_dec = db.query(Decision).filter(Decision.session_id == session_id, Decision.scenario_id == dto.scenario_id).first()
    if existing_dec:
        raise HTTPException(status_code=400, detail="Decision already submitted for this scenario")

    scenario = db.query(Scenario).filter(Scenario.id == dto.scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # Persist decision
    decision = Decision(
        id=str(uuid.uuid4()),
        session_id=session_id,
        scenario_id=dto.scenario_id,
        action=dto.action,
        reason_tags=dto.reason_tags,
        free_text=dto.free_text,
        confidence=dto.confidence,
        latency_ms=dto.latency_ms,
        submitted_at=datetime.now(timezone.utc)
    )
    db.add(decision)
    db.flush()

    # Perform deterministic server-side scoring
    payload = scenario.json_payload
    safe_actions = payload.get("actions", {}).get("safe", [])
    acceptable_actions = payload.get("actions", {}).get("acceptable", [])
    unsafe_actions = payload.get("actions", {}).get("unsafe", [])
    truth = scenario.truth

    # Check evidence opened in telemetry events
    opened_events = (
        db.query(BehaviourEvent)
        .filter(
            BehaviourEvent.session_id == session_id,
            BehaviourEvent.scenario_id == dto.scenario_id,
            BehaviourEvent.event_type == "open_evidence"
        )
        .all()
    )
    opened_ev_ids = set()
    for e in opened_events:
        if e.payload and "evidence_id" in e.payload:
            opened_ev_ids.add(e.payload["evidence_id"])

    # Check official channel evidence
    official_channel_inspected = False
    for ev in scenario.evidence_items:
        raw_id = ev.id.replace(f"{scenario.id}-", "")
        if ev.official_channel and (ev.id in opened_ev_ids or raw_id in opened_ev_ids):
            official_channel_inspected = True
            break

    dq = calculate_decision_quality(dto.action, safe_actions, acceptable_actions, unsafe_actions)
    uc = calculate_under_caution(truth, dto.action, unsafe_actions, official_channel_inspected)
    oc = calculate_over_caution(truth, dto.action, len(opened_ev_ids))
    verified = calculate_independent_verification(dto.action, official_channel_inspected)
    depth = calculate_evidence_depth(len(opened_ev_ids), len(scenario.evidence_items))
    alignment = calculate_reason_alignment(dto.reason_tags, verified)

    outcome = ScenarioOutcome(
        id=str(uuid.uuid4()),
        decision_id=decision.id,
        decision_quality=dq,
        under_caution=uc,
        over_caution=oc,
        verified=verified,
        evidence_depth=depth,
        reason_alignment_flag=alignment
    )
    db.add(outcome)
    db.commit()

    return DecisionOutcomeResponseDTO(decision_id=decision.id, status="recorded")

def get_intervention_content(db: DBSession, session_id: str, user_id: str) -> Dict[str, Any]:
    session = db.query(Session).filter(Session.id == session_id, Session.user_id == user_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.arm == "generic":
        lesson_code = "LESSON_GENERAL_STRATEGY"
    else:
        # Fetch baseline outcomes
        baseline_decisions = (
            db.query(Decision)
            .join(SessionScenario, (SessionScenario.scenario_id == Decision.scenario_id) & (SessionScenario.session_id == Decision.session_id))
            .filter(Decision.session_id == session_id, SessionScenario.phase == "baseline")
            .all()
        )
        baseline_outcomes = []
        for dec in baseline_decisions:
            sc = db.query(Scenario).filter(Scenario.id == dec.scenario_id).first()
            out = db.query(ScenarioOutcome).filter(ScenarioOutcome.decision_id == dec.id).first()
            if sc and out:
                baseline_outcomes.append({
                    "decision_quality": out.decision_quality,
                    "verified": out.verified,
                    "over_caution": out.over_caution,
                    "mechanisms": sc.mechanisms
                })
        lesson_code = select_targeted_intervention(baseline_outcomes)

    lessons_library = {
        "LESSON_LOW_VERIFICATION": {
            "title": "Always Verify Out-of-Band",
            "body": "When receiving urgent or official requests, never use the links or contacts provided in the message. Always verify through an independent official channel.",
            "exercises": ["Identify which channel is independent."]
        },
        "LESSON_AUTH_VULNERABILITY": {
            "title": "Question Authority Claims",
            "body": "Authority claims (bank security, placement office, IT support) should increase your verification effort rather than rushing your trust.",
            "exercises": ["Check official portal before acting."]
        },
        "LESSON_URG_VULNERABILITY": {
            "title": "Slow Down Under Time Pressure",
            "body": "Urgency is designed to force fast, unverified decisions. Legitimate institutions allow adequate time for independent verification.",
            "exercises": ["Spot fake countdown deadlines."]
        },
        "LESSON_REW_VULNERABILITY": {
            "title": "Evaluate Scarcity & Rewards",
            "body": "Unexpected rewards, grants, or exclusive vouchers requiring fast action or personal details carry high phishing risk.",
            "exercises": ["Confirm offers on official brand sites."]
        },
        "LESSON_OVER_CAUTION": {
            "title": "Calibrated Trust: Check Before Rejecting",
            "body": "Over-caution leads to missed genuine notifications. Verify authentic messages on your official portal before ignoring or reporting.",
            "exercises": ["Confirm authentic portal notices."]
        },
        "LESSON_GENERAL_STRATEGY": {
            "title": "General Verification Tip Sheet",
            "body": "Check sender domains, verify links on official portals, look out for unexpected attachments, and use independent channels to confirm requests.",
            "exercises": ["Review core security guidelines."]
        }
    }

    content = lessons_library.get(lesson_code, lessons_library["LESSON_GENERAL_STRATEGY"])
    return {
        "session_id": session_id,
        "arm": session.arm,
        "lesson_code": lesson_code,
        "content": content
    }

def complete_intervention(db: DBSession, session_id: str, user_id: str, practice_score: int = 100) -> Dict[str, Any]:
    session = db.query(Session).filter(Session.id == session_id, Session.user_id == user_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # DEFECT 3 FIX: Intervention Phase Enforcement
    if session.current_phase != "intervention":
        raise HTTPException(status_code=400, detail="Session is not in intervention phase")

    delivery = db.query(InterventionDelivery).filter(InterventionDelivery.session_id == session_id).first()
    if not delivery:
        content = get_intervention_content(db, session_id, user_id)
        delivery = InterventionDelivery(
            id=str(uuid.uuid4()),
            session_id=session_id,
            intervention_type=session.arm,
            lesson_code=content["lesson_code"],
            practice_score=practice_score,
            completed_at=datetime.now(timezone.utc)
        )
        db.add(delivery)

    session.current_phase = "retest"
    db.commit()

    return {"session_id": session_id, "status": "intervention_completed", "next_phase": "retest"}

def calculate_resilience_profile(db: DBSession, session_id: str, user_id: str) -> Dict[str, Any]:
    session = db.query(Session).filter(Session.id == session_id, Session.user_id == user_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    phases = ["baseline", "retest", "transfer"]
    profile_data = {}

    for ph in phases:
        decisions = (
            db.query(Decision)
            .join(SessionScenario, (SessionScenario.scenario_id == Decision.scenario_id) & (SessionScenario.session_id == Decision.session_id))
            .filter(Decision.session_id == session_id, SessionScenario.phase == ph)
            .all()
        )
        if not decisions:
            continue

        outcomes = []
        malicious_outcomes = []
        genuine_outcomes = []
        cal_errors = []

        for dec in decisions:
            out = db.query(ScenarioOutcome).filter(ScenarioOutcome.decision_id == dec.id).first()
            sc = db.query(Scenario).filter(Scenario.id == dec.scenario_id).first()
            if out and sc:
                outcomes.append(out)

                if sc.truth == "malicious":
                    malicious_outcomes.append({"under_caution": out.under_caution})
                elif sc.truth == "genuine":
                    genuine_outcomes.append({"over_caution": out.over_caution})

                # Confidence Calibration Error calculation:
                # Normalized Confidence (scale 1..5 mapped to 0.0..1.0) - Decision Quality (0.0..1.0)
                norm_conf = (dec.confidence - 1.0) / 4.0
                cal_errors.append(norm_conf - out.decision_quality)

        if outcomes:
            mean_dq = sum(o.decision_quality for o in outcomes) / len(outcomes)
            verified_rate = sum(1 for o in outcomes if o.verified) / len(outcomes)
            under_caution_count = sum(1 for o in outcomes if o.under_caution)
            over_caution_count = sum(1 for o in outcomes if o.over_caution)
            mean_depth = sum(o.evidence_depth for o in outcomes) / len(outcomes)

            sdt_res = calculate_sdt_metrics(malicious_outcomes, genuine_outcomes)
            mean_cal_error = round(sum(cal_errors) / len(cal_errors), 4) if cal_errors else None

            metrics = {
                "count": len(outcomes),
                "decision_quality_mean": round(mean_dq, 4),
                "verification_rate": round(verified_rate, 4),
                "under_caution_count": under_caution_count,
                "over_caution_count": over_caution_count,
                "evidence_depth_mean": round(mean_depth, 4),
                "d_prime": sdt_res["d_prime"],
                "criterion_c": sdt_res["criterion_c"],
                "confidence_calibration_error": mean_cal_error
            }
            profile_data[ph] = metrics

            existing_prof = (
                db.query(ResilienceProfile)
                .filter(ResilienceProfile.session_id == session_id, ResilienceProfile.phase == ph)
                .first()
            )
            if existing_prof:
                existing_prof.metrics_json = metrics
            else:
                prof = ResilienceProfile(
                    id=str(uuid.uuid4()),
                    session_id=session_id,
                    phase=ph,
                    metrics_json=metrics
                )
                db.add(prof)

    db.commit()

    return {
        "session_id": session_id,
        "completed_at": session.completed_at.isoformat() if session.completed_at else None,
        "profile": profile_data
    }
