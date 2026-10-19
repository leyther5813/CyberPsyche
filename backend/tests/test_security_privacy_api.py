import pytest
from app.core.database import SessionLocal
from app.models.user import User

def test_security_access_control_and_privacy_deletion(client):
    # 1. Unauthorized endpoint access
    unauth_resp = client.get("/api/v1/sessions/nonexistent/next")
    assert unauth_resp.status_code == 401

    # 2. Participant role cannot access /research/export
    part_email = "participant_user_99@example.com"
    part_pass = "Password123!"
    reg = client.post("/api/v1/auth/register", json={"email": part_email, "password": part_pass}).json()
    part_token = reg["access_token"]

    export_denied = client.get("/api/v1/research/export", headers={"Authorization": f"Bearer {part_token}"})
    assert export_denied.status_code == 403

    # 3. Create Researcher user in DB and verify /research/export access
    db = SessionLocal()
    try:
        res_email = "researcher_admin@example.com"
        res_pass = "ResearcherPass123!"
        reg_res = client.post("/api/v1/auth/register", json={"email": res_email, "password": res_pass}).json()
        res_id = reg_res["user"]["id"]
        
        # Promote to researcher
        user_obj = db.query(User).filter(User.id == res_id).first()
        user_obj.role = "researcher"
        db.commit()

        # Login again to get updated token with researcher role
        res_token = client.post("/api/v1/auth/login", json={"email": res_email, "password": res_pass}).json()["access_token"]
        
        export_allowed = client.get("/api/v1/research/export", headers={"Authorization": f"Bearer {res_token}"})
        assert export_allowed.status_code == 200
        assert export_allowed.headers["content-type"].startswith("text/csv")
    finally:
        db.close()

    # 4. Delete Me (Data minimization / privacy compliance)
    del_resp = client.delete("/api/v1/privacy/delete-me", headers={"Authorization": f"Bearer {part_token}"})
    assert del_resp.status_code == 200
    assert del_resp.json()["status"] == "deleted"

    # Verify user can no longer log in or access protected endpoints
    login_after_del = client.post("/api/v1/auth/login", json={"email": part_email, "password": part_pass})
    assert login_after_del.status_code == 401
