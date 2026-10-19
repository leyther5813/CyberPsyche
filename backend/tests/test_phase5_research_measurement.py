import csv
import io
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.core.security import hash_password, create_access_token
from app.models.user import User, Consent
from app.models.scenario import Scenario
from app.models.session import Session, SessionScenario
from app.models.behaviour import Decision, ScenarioOutcome
from app.scoring.constructs import calculate_reason_alignment
from app.services.session_service import create_session, get_next_scenario, submit_decision, calculate_resilience_profile

client = TestClient(app)

def test_reasoning_alignment_recognizes_verification_tag():
    """Verify calculate_reason_alignment correctly handles approved verification tags."""
    tag = "Requires verification on official institutional portal"
    
    # Contradiction: claimed verification tag, but verified is False -> False
    assert calculate_reason_alignment([tag], verified=False) is False
    
    # Aligned: claimed verification tag, and verified is True -> True
    assert calculate_reason_alignment([tag], verified=True) is True
    
    # Aligned: non-verification tag -> True
    assert calculate_reason_alignment(["Routine communication"], verified=False) is True

def test_research_export_contains_required_metadata_and_security(db_session):
    """Verify research export CSV includes enriched scenario metadata while keeping security & pseudonymity intact."""
    db = db_session

    # Create participant user
    part_user = User(
        email_hash="hash_participant_123",
        password_hash=hash_password("Password123!"),
        role="participant"
    )
    # Create researcher user
    res_user = User(
        email_hash="hash_researcher_456",
        password_hash=hash_password("Password123!"),
        role="researcher"
    )
    db.add(part_user)
    db.add(res_user)
    db.commit()

    # Research consent requirement
    db.add(Consent(user_id=part_user.id, version="1.0"))
    db.commit()

    # Create session for participant
    session = create_session(db, user_id=part_user.id, arm="targeted", form_assignment="Form_A")
    sc = db.query(SessionScenario).filter(SessionScenario.session_id == session.id, SessionScenario.phase == "baseline").order_by(SessionScenario.order_idx).first()

    submit_decision(db, session_id=session.id, user_id=part_user.id, dto=type("DTO", (), {
        "scenario_id": sc.scenario_id,
        "action": "VERIFY_INDEPENDENTLY",
        "reason_tags": ["Requires verification on official institutional portal"],
        "free_text": "Verified on portal",
        "confidence": 4,
        "latency_ms": 1200
    }))

    # 1. Verify participant token receives 403 Forbidden on export
    part_token = create_access_token(subject=part_user.id, role=part_user.role)
    res_part = client.get("/api/v1/research/export", headers={"Authorization": f"Bearer {part_token}"})
    assert res_part.status_code == 403

    # 2. Verify researcher token receives 200 OK on export
    res_token = create_access_token(subject=res_user.id, role=res_user.role)
    res_export = client.get("/api/v1/research/export", headers={"Authorization": f"Bearer {res_token}"})
    assert res_export.status_code == 200
    
    csv_text = res_export.text
    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)
    header = rows[0]

    # Verify required columns are present
    required_cols = ["phase", "truth", "pressure", "mechanisms", "family_id", "context", "channel"]
    for col in required_cols:
        assert col in header, f"Missing required column '{col}' in research CSV export"

    # Verify pseudonymisation (email_hash included, no raw email/passwords)
    assert "pseudonym_user_hash" in header
    assert "password_hash" not in header
    assert "password" not in header

def test_sdt_and_confidence_calibration_in_resilience_profile(db_session):
    """Verify SDT (d_prime, criterion_c) and confidence_calibration_error are attached to profile JSON."""
    db = db_session

    part_user = User(
        email_hash="hash_sdt_participant",
        password_hash=hash_password("Password123!"),
        role="participant"
    )
    db.add(part_user)
    db.commit()

    db.add(Consent(user_id=part_user.id, version="1.0"))
    db.commit()

    session = create_session(db, user_id=part_user.id, arm="targeted", form_assignment="Form_A")
    baseline_scenarios = db.query(SessionScenario).filter(SessionScenario.session_id == session.id, SessionScenario.phase == "baseline").all()

    # Submit decisions for baseline scenarios
    for ss in baseline_scenarios:
        submit_decision(db, session_id=session.id, user_id=part_user.id, dto=type("DTO", (), {
            "scenario_id": ss.scenario_id,
            "action": "VERIFY_INDEPENDENTLY",
            "reason_tags": ["Requires verification on official institutional portal"],
            "free_text": "Verified.",
            "confidence": 5,
            "latency_ms": 2000
        }))

    # Calculate resilience profile
    profile_resp = calculate_resilience_profile(db, session_id=session.id, user_id=part_user.id)
    assert "profile" in profile_resp
    assert "baseline" in profile_resp["profile"]

    b_metrics = profile_resp["profile"]["baseline"]
    assert "d_prime" in b_metrics
    assert "criterion_c" in b_metrics
    assert "confidence_calibration_error" in b_metrics

    assert isinstance(b_metrics["d_prime"], float)
    assert isinstance(b_metrics["criterion_c"], float)
    assert isinstance(b_metrics["confidence_calibration_error"], float)

def test_participant_endpoints_do_not_expose_protected_metadata(db_session):
    """Verify participant next scenario and event endpoints strictly omit protected metadata."""
    db = db_session

    user = User(email_hash="hash_part_protect", password_hash=hash_password("Password123!"), role="participant")
    db.add(user)
    db.commit()

    db.add(Consent(user_id=user.id, version="1.0"))
    db.commit()

    session = create_session(db, user_id=user.id, arm="targeted", form_assignment="Form_A")
    token = create_access_token(subject=user.id, role=user.role)

    # Next scenario request
    res = client.get(f"/api/v1/sessions/{session.id}/next", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()

    protected_fields = ["truth", "signal", "diagnosticity", "official_channel", "mechanisms", "actions"]
    for field in protected_fields:
        assert field not in data, f"SECURITY AUDIT DEFECT: '{field}' exposed in participant next scenario endpoint"
