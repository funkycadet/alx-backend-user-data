#!/usr/bin/env python3
"""
Main module
"""

import requests


def register_user(email: str, password: str) -> None:
    """
    Test to register a user with given email and password
    """
    response = requests.post(
        'http://127.0.0.1:5000/users',
        data={"email": email, "password": password}
    )
    if response.status_code == 200:
        assert(response.json() == {"email": email, "message": "user created"})
    else:
        assert(response.status_code == 400)
        assert(response.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """
    """
    response = requests.post(
        'http://127.0.0.1:5000/sessions',
        data={'email': email, 'password': password}
    )
    assert (response.status_code == 401)


def log_in(email: str, password: str) -> str:
    """
    """
    response = requests.post(
        'http://127.0.0.1:5000/sessions',
        data={'email': email, 'password': password}
    )
    assert (response.status_code == 200)
    assert(response.json() == {"email": email, "message": "logged in"})
    return response.cookies['session_id']


def profile_unlogged() -> None:
    """
    """
    response = requests.get('http://127.0.0.1:5000/profile')
    assert(response.status_code == 403)


def profile_logged(session_id: str) -> None:
    """
    """
    cookies = {'session_id': session_id}
    response = requests.get(
        'http://127.0.0.1:5000/profile',
        cookies=cookies
    )
    assert(response.status_code == 200)


def log_out(session_id: str) -> None:
    """
    """
    cookies = {'session_id': session_id}
    response = requests.delete(
        'http://127.0.0.1:5000/sessions',
        cookies=cookies
    )
    if response.status_code == 302:
        assert(response.url == 'http://127.0.0.1:5000/')
    else:
        assert(response.status_code == 200)


def reset_password_token(email: str) -> str:
    """
    """
    response = requests.post(
        'http://127.0.0.1:5000/reset_password',
        data={'email': email}
    )
    if response.status_code == 200:
        return response.json()['reset_token']
    assert(response.status_code == 401)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    """
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    response = requests.put('http://127.0.0.1:5000/reset_password', data=data)
    if response.status_code == 200:
        assert(response.json() == {
            "email": email,
            "message": "Password updated"
        })
    else:
        assert(response.status_code == 403)


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
