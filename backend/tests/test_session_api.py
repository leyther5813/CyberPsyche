import pytest

def test_complete_study_session_pipeline_and_integrity(client):
    email = "study_participant_full@example.com"
    password = "SecurePassword123!"

    # 1. Register and Consent
    reg = client.post("/api/v1/auth/register", json={"email": email, "password": password}).json()
    token = reg["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/api/v1/consent", json={"version": "1.0", "accepted": True}, headers=headers)

    # 2. Start Session
    sess_resp = client.post("/api/v1/sessions", json={"arm": "targeted", "form_assignment": "Form_A"}, headers=headers)
    assert sess_resp.status_code == 200, sess_resp.text
    session_data = sess_resp.json()
    session_id = session_data["session_id"]
    assert session_data["current_phase"] == "baseline"

    # 3. Fetch Next Scenario (Baseline Phase)
    next_resp = client.get(f"/api/v1/sessions/{session_id}/next", headers=headers)
    assert next_resp.status_code == 200, next_resp.text
    sc_data = next_resp.json()

    # --- CRITICAL RESEARCH INTEGRITY CHECKS ---
    assert "truth" not in sc_data, "SECURITY DEFECT: Ground truth leaked in participant response!"
    assert "mechanisms" not in sc_data, "SECURITY DEFECT: Mechanisms leaked in participant response!"
    assert "actions" not in sc_data or not isinstance(sc_data.get("actions"), dict), "SECURITY DEFECT: Action safety classifications leaked!"
    
    # Verify evidence items are scrubbed (no signal, no diagnosticity, no value before opening)
    for ev in sc_data["available_evidence"]:
        assert "signal" not in ev, "SECURITY DEFECT: Evidence signal leaked!"
        assert "diagnosticity" not in ev, "SECURITY DEFECT: Evidence diagnosticity leaked!"
        assert "value" not in ev, "SECURITY DEFECT: Evidence value leaked before opening!"
        assert "id" in ev
        assert "label" in ev

    scenario_id = sc_data["scenario_id"]
    ev_id = sc_data["available_evidence"][0]["id"]

    # 4. Open Evidence (Telemetry + Revealing value)
    event_payload = {
        "scenario_id": scenario_id,
        "event_type": "open_evidence",
        "payload": {"evidence_id": ev_id}
    }
    ev_resp = client.post(f"/api/v1/sessions/{session_id}/events", json=event_payload, headers=headers)
    assert ev_resp.status_code == 200
    ev_json = ev_resp.json()
    assert "revealed_evidence" in ev_json
    assert ev_json["revealed_evidence"]["id"] == ev_id
    assert "value" in ev_json["revealed_evidence"]

    # 5. Submit Decision for Baseline Scenario
    dec_payload = {
        "scenario_id": scenario_id,
        "action": "VERIFY_INDEPENDENTLY",
        "reason_tags": ["I verified independently"],
        "free_text": "Checked the portal",
        "confidence": 5,
        "latency_ms": 12000
    }
    dec_resp = client.post(f"/api/v1/sessions/{session_id}/decision", json=dec_payload, headers=headers)
    assert dec_resp.status_code == 200
    assert dec_resp.json()["status"] == "recorded"

    # Duplicate decision submission fails
    dup_dec = client.post(f"/api/v1/sessions/{session_id}/decision", json=dec_payload, headers=headers)
    assert dup_dec.status_code == 400

    # 6. Complete remaining baseline scenarios
    for _ in range(5):
        nxt = client.get(f"/api/v1/sessions/{session_id}/next", headers=headers).json()
        if nxt.get("status") == "phase_completed":
            break
        sc_id = nxt["scenario_id"]
        client.post(f"/api/v1/sessions/{session_id}/decision", json={
            "scenario_id": sc_id,
            "action": "VERIFY_INDEPENDENTLY",
            "reason_tags": ["I verified independently"],
            "confidence": 4,
            "latency_ms": 8000
        }, headers=headers)

    # Call /next to trigger phase transition to intervention phase
    phase_trans = client.get(f"/api/v1/sessions/{session_id}/next", headers=headers).json()
    assert phase_trans.get("current_phase") == "intervention"

    # 7. Check Intervention
    interv_resp = client.get(f"/api/v1/sessions/{session_id}/intervention", headers=headers)
    assert interv_resp.status_code == 200
    interv_json = interv_resp.json()
    assert "lesson_code" in interv_json

    # Complete Intervention
    comp_interv = client.post("/api/v1/intervention/complete", json={"session_id": session_id, "practice_score": 100}, headers=headers)
    assert comp_interv.status_code == 200
    assert comp_interv.json()["next_phase"] == "retest"

    # 8. Check Session Profile
    prof_resp = client.get(f"/api/v1/sessions/{session_id}/profile", headers=headers)
    assert prof_resp.status_code == 200
    prof_json = prof_resp.json()
    assert "profile" in prof_json
    assert "baseline" in prof_json["profile"]
    assert prof_json["profile"]["baseline"]["count"] == 6
    assert "verification_rate" in prof_json["profile"]["baseline"]
