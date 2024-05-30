#!/usr/bin/env python3
"""End-to-end integration test"""
import requests

HOST = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test user registeration"""
    url = f"{HOST}/users"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    response = requests.post(url, data=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with wrong password"""
    url = f"{HOST}/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 401


def profile_unlogged() -> None:
    """Test profile route"""
    url = f"{HOST}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test profile route"""
    url = f"{HOST}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """Test logout of a session."""
    url = f"{HOST}/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Tests requesting a password reset."""
    url = f"{HOST}/reset_password"
    payload = {"email": email}
    response = requests.post(url, data=payload)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == email
    assert "reset_token" in response.json()
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests updating a user's password."""
    url = f"{HOST}/reset_password"
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password,
    }
    response = requests.put(url, data=payload)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


def log_in(email: str, password: str) -> str:
    """Tests login"""
    url = f"{HOST}/sessions"
    payload = {
        "email": email,
        "password": password,
    }
    response = requests.post(url, data=payload)
    session_id = requests.get("session_id", None)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    assert session_id is not None
    return session_id


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
