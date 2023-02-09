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
