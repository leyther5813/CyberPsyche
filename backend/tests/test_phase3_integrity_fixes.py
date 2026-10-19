import pytest
from app.core.database import SessionLocal
from app.models.scenario import Scenario
from app.models.session import Session, SessionScenario
from app.services.session_service import create_session

def test_evidence_gating_integrity_and_edge_cases(client):
    """Verifies Defect 1 Fixes for Evidence Gating Security."""
    # Participant 1 setup
    user1_email = "part1_gating@example.com"
    user1_pass = "Password123!"
    reg1 = client.post("/api/v1/auth/register", json={"email": user1_email, "password": user1_pass}).json()
    token1 = reg1["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    client.post("/api/v1/consent", json={"accepted": True}, headers=headers1)

    sess1 = client.post("/api/v1/sessions", json={"arm": "targeted", "form_assignment": "Form_A"}, headers=headers1).json()
    sess1_id = sess1["session_id"]

    # Participant 2 setup
    user2_email = "part2_gating@example.com"
    user2_pass = "Password123!"
    reg2 = client.post("/api/v1/auth/register", json={"email": user2_email, "password": user2_pass}).json()
    token2 = reg2["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}
    client.post("/api/v1/consent", json={"accepted": True}, headers=headers2)

    sess2 = client.post("/api/v1/sessions", json={"arm": "targeted", "form_assignment": "Form_A"}, headers=headers2).json()
    sess2_id = sess2["session_id"]

    # Fetch next scenario for Participant 1
    sc1 = client.get(f"/api/v1/sessions/{sess1_id}/next", headers=headers1).json()
    sc1_id = sc1["scenario_id"]
    ev1_id = sc1["available_evidence"][0]["id"]

    # Fetch next scenario for Participant 2
    sc2 = client.get(f"/api/v1/sessions/{sess2_id}/next", headers=headers2).json()
    sc2_id = sc2["scenario_id"]

    # 1. Valid evidence opening by Participant 1
    valid_ev = client.post(f"/api/v1/sessions/{sess1_id}/events", json={
        "scenario_id": sc1_id,
        "event_type": "open_evidence",
        "payload": {"evidence_id": ev1_id}
    }, headers=headers1)
    assert valid_ev.status_code == 200
    assert "revealed_evidence" in valid_ev.json()
    rev = valid_ev.json()["revealed_evidence"]
    assert "signal" not in rev
    assert "diagnosticity" not in rev
    assert "truth" not in rev

    # 2. Reject wrong scenario ID
    wrong_sc = client.post(f"/api/v1/sessions/{sess1_id}/events", json={
        "scenario_id": "NON_EXISTENT_SCENARIO_99",
        "event_type": "open_evidence",
        "payload": {"evidence_id": "e1"}
    }, headers=headers1)
    assert wrong_sc.status_code == 400

    # 3. Reject opening evidence for another participant's scenario/session
    cross_part = client.post(f"/api/v1/sessions/{sess1_id}/events", json={
        "scenario_id": sc2_id,
        "event_type": "open_evidence",
        "payload": {"evidence_id": "e1"}
    }, headers=headers2)
    assert cross_part.status_code == 404

    # 4. Reject opening evidence for an inactive scenario in the same session (e.g. retest scenario during baseline)
    db = SessionLocal()
    try:
        retest_ss = db.query(SessionScenario).filter(SessionScenario.session_id == sess1_id, SessionScenario.phase == "retest").first()
        retest_sc_id = retest_ss.scenario_id
        
        inactive_sc = client.post(f"/api/v1/sessions/{sess1_id}/events", json={
            "scenario_id": retest_sc_id,
            "event_type": "open_evidence",
            "payload": {"evidence_id": "e1"}
        }, headers=headers1)
        assert inactive_sc.status_code == 400
    finally:
        db.close()

    # 5. Reject evidence opening AFTER decision submission
    client.post(f"/api/v1/sessions/{sess1_id}/decision", json={
        "scenario_id": sc1_id,
        "action": "VERIFY_INDEPENDENTLY",
        "reason_tags": ["I verified independently"],
        "confidence": 5,
        "latency_ms": 5000
    }, headers=headers1)

    post_dec_ev = client.post(f"/api/v1/sessions/{sess1_id}/events", json={
        "scenario_id": sc1_id,
        "event_type": "open_evidence",
        "payload": {"evidence_id": ev1_id}
    }, headers=headers1)
    assert post_dec_ev.status_code == 400

def test_deterministic_family_ordering(client):
    """Verifies Defect 2 Fix for Deterministic Family Ordering."""
    user_email = "deterministic_order@example.com"
    user_pass = "Password123!"
    reg = client.post("/api/v1/auth/register", json={"email": user_email, "password": user_pass}).json()
    token = reg["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/v1/consent", json={"accepted": True}, headers=headers)

    # Form_A session
    sess_a = client.post("/api/v1/sessions", json={"arm": "targeted", "form_assignment": "Form_A"}, headers=headers).json()
    sess_a_id = sess_a["session_id"]

    # Form_B session
    sess_b = client.post("/api/v1/sessions", json={"arm": "targeted", "form_assignment": "Form_B"}, headers=headers).json()
    sess_b_id = sess_b["session_id"]

    db = SessionLocal()
    try:
        # Check Form_A baseline scenario family order
        ss_a = db.query(SessionScenario).filter(SessionScenario.session_id == sess_a_id, SessionScenario.phase == "baseline").order_by(SessionScenario.order_idx).all()
        a_fams = [db.query(Scenario).filter(Scenario.id == item.scenario_id).first().family_id for item in ss_a]
        
        # Check Form_B baseline scenario family order
        ss_b = db.query(SessionScenario).filter(SessionScenario.session_id == sess_b_id, SessionScenario.phase == "baseline").order_by(SessionScenario.order_idx).all()
        b_fams = [db.query(Scenario).filter(Scenario.id == item.scenario_id).first().family_id for item in ss_b]

        # Verify families are sorted deterministically
        assert len(a_fams) == 6
        assert len(b_fams) == 6
        assert a_fams == sorted(a_fams)
    finally:
        db.close()

def test_intervention_phase_enforcement_and_abuse_prevention(client):
    """Verifies Defect 3 Fix for Intervention Phase Enforcement."""
    user_email = "interv_abuse@example.com"
    user_pass = "Password123!"
    reg = client.post("/api/v1/auth/register", json={"email": user_email, "password": user_pass}).json()
    token = reg["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/v1/consent", json={"accepted": True}, headers=headers)

    sess = client.post("/api/v1/sessions", json={"arm": "targeted", "form_assignment": "Form_A"}, headers=headers).json()
    sess_id = sess["session_id"]

    # 1. Reject completing intervention during baseline phase
    bad_baseline = client.post("/api/v1/intervention/complete", json={"session_id": sess_id}, headers=headers)
    assert bad_baseline.status_code == 400

    # Complete 6 baseline scenarios to move to intervention phase
    for _ in range(6):
        sc = client.get(f"/api/v1/sessions/{sess_id}/next", headers=headers).json()
        if sc.get("status") == "phase_completed":
            break
        sc_id = sc["scenario_id"]
        client.post(f"/api/v1/sessions/{sess_id}/decision", json={
            "scenario_id": sc_id,
            "action": "VERIFY_INDEPENDENTLY",
            "reason_tags": ["I verified independently"],
            "confidence": 4,
            "latency_ms": 5000
        }, headers=headers)

    # Verify session is now in intervention phase
    nxt = client.get(f"/api/v1/sessions/{sess_id}/next", headers=headers).json()
    assert nxt["current_phase"] == "intervention"

    # 2. Valid intervention completion
    valid_interv = client.post("/api/v1/intervention/complete", json={"session_id": sess_id}, headers=headers)
    assert valid_interv.status_code == 200
    assert valid_interv.json()["next_phase"] == "retest"

    # 3. Reject completing intervention twice (now session is in retest phase)
    double_interv = client.post("/api/v1/intervention/complete", json={"session_id": sess_id}, headers=headers)
    assert double_interv.status_code == 400
