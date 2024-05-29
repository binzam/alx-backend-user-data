#!/usr/bin/env python3
"""End-to-end integration test"""
import requests


def register_user(email: str, password: str) -> None:
    """Test user registeration"""
    url = "{}/users".format(HOST)
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    response = requests.post(url, data=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
HOST = "http://0.0.0.0:5000"

if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    # log_in_wrong_password(EMAIL, NEW_PASSWD)
    # profile_unlogged()
    # session_id = log_in(EMAIL, PASSWD)
    # profile_logged(session_id)
    # log_out(session_id)
    # reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)
