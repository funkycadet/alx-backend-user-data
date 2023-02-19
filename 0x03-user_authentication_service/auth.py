#!/usr/bin/env python3
""" Auth module
"""
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User

import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """ _hash_password method
    Returns given password strings as bytes
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _generate_uuid(self):
        """ _generate_uuid method
        Generates UUID
        """
        new_uuid = uuid.uuid4()
        return new_uuid

    def register_user(self, email: str, password: str) -> User:
        """ register_user method
        Registers a new user and saves to db
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ valid_login method
        Checks the validity of the given email and password
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        user_password = user.hashed_password
        password_check = password.encode('utf-8')
        return bcrypt.checkpw(password_check, user_password)
