#!/usr/bin/env python3
""" Auth module
"""
import bcrypt


def _hash_password(password):
    """ _hash_password method
    Returns given password strings as bytes
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password
