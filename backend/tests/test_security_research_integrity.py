import pytest
from app.schemas.scenario_schema import ScrubbedNextScenarioResponse, EvidenceItemScrubbed
from app.core.security import generate_csrf_token, verify_csrf_token, create_access_token, decode_access_token

def test_ground_truth_not_leaked_in_next_scenario_schema():
    """Verify ScrubbedNextScenarioResponse schema excludes truth, signal, and safe/unsafe action classifications."""
    response_data = {
        "session_id": "test-session-123",
        "scenario_id": "EDU-AUTH-URG-MAL-01",
        "phase": "baseline",
        "context": "education_career",
        "channel": "email",
        "persona": "college student (fictional)",
        "pressure": "high",
        "narrative": "Placement coordinator emails a shortlist notice.",
        "message": {
            "sender_display": "Placement Cell",
            "body": "Confirm within 20 minutes."
        },
        "available_evidence": [
            {"id": "e1", "label": "Sender address"}
        ]
    }
    
    dto = ScrubbedNextScenarioResponse(**response_data)
    dump = dto.model_dump()
    
    # Ensure protected research metadata fields do NOT exist in participant-facing payload
    assert "truth" not in dump
    assert "signal" not in dump["available_evidence"][0]
    assert "diagnosticity" not in dump["available_evidence"][0]
    assert "official_channel" not in dump["available_evidence"][0]
    assert "value" not in dump["available_evidence"][0]
    assert "safe_actions" not in dump
    assert "unsafe_actions" not in dump

def test_csrf_token_validation():
    """Verify HMAC CSRF token generation and validation for cookie-based authentication."""
    session_id = "sess-uuid-9999"
    token = generate_csrf_token(session_id)
    
    assert verify_csrf_token(session_id, token) is True
    assert verify_csrf_token("different-session-id", token) is False
    assert verify_csrf_token(session_id, "invalid-token") is False

def test_jwt_role_embedding():
    """Verify JWT access token embeds sub and role securely."""
    user_id = "user-123"
    token = create_access_token(subject=user_id, role="participant")
    payload = decode_access_token(token)
    
    assert payload is not None
    assert payload["sub"] == user_id
    assert payload["role"] == "participant"
