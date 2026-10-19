import pytest

def test_consent_and_digital_context(client):
    email = "onboarding_user@example.com"
    password = "SecurePassword123!"

    reg = client.post("/api/v1/auth/register", json={"email": email, "password": password}).json()
    token = reg["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Accept Consent
    consent_resp = client.post("/api/v1/consent", json={"version": "1.0", "accepted": True}, headers=headers)
    assert consent_resp.status_code == 200
    assert consent_resp.json()["status"] == "accepted"

    # 2. Rejecting consent fails
    no_consent = client.post("/api/v1/consent", json={"version": "1.0", "accepted": False}, headers=headers)
    assert no_consent.status_code == 400

    # 3. Update Digital Context
    context_data = {
        "life_stage": "undergraduate_student",
        "activities": ["online_banking", "social_media"],
        "cyber_level": "intermediate",
        "interests": ["computer_science"]
    }
    ctx_resp = client.put("/api/v1/context", json=context_data, headers=headers)
    assert ctx_resp.status_code == 200
    assert ctx_resp.json()["status"] == "updated"
