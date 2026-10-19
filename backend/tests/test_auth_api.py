import pytest

def test_user_registration_and_login(client):
    email = "participant_test_100@example.com"
    password = "SecurePassword123!"

    # 1. Register
    resp = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "access_token" in data
    assert "user" in data
    assert data["user"]["role"] == "participant"

    # 2. Duplicate registration fails
    dup_resp = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert dup_resp.status_code == 400

    # 3. Login
    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert "access_token" in login_data

    # 4. Login with invalid password fails
    bad_login = client.post("/api/v1/auth/login", json={"email": email, "password": "WrongPassword!"})
    assert bad_login.status_code == 401

    # 5. Logout
    logout_resp = client.post("/api/v1/auth/logout")
    assert logout_resp.status_code == 200
