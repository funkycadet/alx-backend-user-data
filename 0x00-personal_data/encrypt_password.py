#!/usr/bin/env python3
""" Encrypt password module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash_password function
    This function converts password to utf-8 encoding and hashes
    it using hashpw function from bcrypt module
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ is_valid function
    This function validates if the password if valid after
    being hashed
    """
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False
