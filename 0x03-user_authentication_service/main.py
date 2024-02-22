#!/usr/bin/env python3
"""
Main file
"""

import requests

# Register a new user
def register_user(email: str, password: str) -> None:
    # Send POST request
    response = requests.post(
        'http://localhost:5000/users',
        data={'email': email, 'password': password}
    )
    # Assert status code and response
    assert response.status_code == 200
    assert response.json() == {
        "email": email,
        "message": "user created"
    }

# Log in with wrong password
def log_in_wrong_password(email: str, password: str) -> None:
    # Send POST request
    response = requests.post(
        'http://localhost:5000/sessions',
        data={'email': email, 'password': password}
    )
    # Assert status code
    assert response.status_code == 401

# Log in with correct credentials
def log_in(email: str, password: str) -> str:
    # Send POST request
    response = requests.post(
        'http://localhost:5000/sessions',
        data={'email': email, 'password': password}
    )
    # Assert status code and response
    assert response.status_code == 200
    assert response.json() == {
        "email": email,
        "message": "Logged in"
    }
    # Return session ID
    return response.cookies.get('session_id')

# Access profile without logging in
def profile_unlogged() -> None:
    # Send GET request
    response = requests.get('http://localhost:5000/profile')
    # Assert status code
    assert response.status_code == 403

# Access profile after logging in
def profile_logged(session_id: str) -> None:
    # Send GET request
    response = requests.get(
        'http://localhost:5000/profile',
        cookies={'session_id': session_id}
    )
    # Assert status code
    assert response.status_code == 200

# Log out
def log_out(session_id: str) -> None:
    # Send DELETE request
    response = requests.delete(
        'http://localhost:5000/sessions',
        cookies={'session_id': session_id}
    )
    # Assert status code
    assert response.status_code == 302

# Get reset password token
def reset_password_token(email: str) -> str:
    # Send POST request
    response = requests.post(
        'http://localhost:5000/reset_password',
        data={'email': email}
    )
    # Assert status code
    assert response.status_code == 200
    # Return reset token
    return response.json().get('reset_token')

# Update password
def update_password(email: str, reset_token: str, new_password: str) -> None:
    # Send PUT request
    response = requests.put(
        'http://localhost:5000/reset_password',
        data={
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password
        }
    )
    # Assert status code and response
    assert response.status_code == 200
    assert response.json() == {
        "email": email,
        "message": "Password updated"
    }

if __name__ == "__main__":
    EMAIL = "guillaume@holberton.io"
    PASSWD = "b4l0u"
    NEW_PASSWD = "t4rt1fl3tt3"

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
