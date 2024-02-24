#!/usr/bin/env python3
"""A simple end-to-end (E2E) integration test for `app.py`.
"""
import requests

# Replace 'http://localhost:5000' with the appropriate URL for your Flask app
BASE_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """Registers a new user."""
    url = f"{BASE_URL}/register"
    payload = {'email': email, 'password': password}
    response = requests.post(url, json=payload)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempts to log in with the wrong password."""
    url = f"{BASE_URL}/login"
    payload = {'email': email, 'password': password}
    response = requests.post(url, json=payload)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Logs in a user and returns the session ID."""
    url = f"{BASE_URL}/login"
    payload = {'email': email, 'password': password}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    return response.json()['session_id']


def profile_unlogged() -> None:
    """Attempts to access the profile page without logging in."""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 401


def profile_logged(session_id: str) -> None:
    """Accesses the profile page after logging in."""
    url = f"{BASE_URL}/profile"
    headers = {'session_id': session_id}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """Logs out a user."""
    url = f"{BASE_URL}/logout"
    headers = {'session_id': session_id}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Gets the reset password token for a user."""
    url = f"{BASE_URL}/reset_password"
    payload = {'email': email}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    return response.json()['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Updates the password for a user."""
    url = f"{BASE_URL}/update_password"
    payload = {'email': email, 'reset_token': reset_token, 'new_password': new_password}
    response = requests.post(url, json=payload)
    assert response.status_code == 200

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
