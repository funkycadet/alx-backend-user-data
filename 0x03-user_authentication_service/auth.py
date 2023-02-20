#!/usr/bin/env python3
"""
Auth module
"""
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
from uuid import uuid4

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Returns given password strings as bytes
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    Generates UUID
    """
    return str(uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
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
        """
        Checks the validity of the given email and password
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        user_password = user.hashed_password
        password_check = password.encode('utf-8')
        return bcrypt.checkpw(password_check, user_password)

    def create_session(self, email: str) -> Union[None, str]:
        """
        Creates a new session for user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Retrieves the user based on the session id available
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user
