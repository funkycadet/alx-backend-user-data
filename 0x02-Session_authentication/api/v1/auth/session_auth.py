#!/usr/bin/env python3
""" Session Authentication module
"""
from .auth import Auth
from typing import TypeVar
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create_session method
        Creates a new session id for users
        """
        if user_id is None:
            return None
        if type(user_id) != str:
            return None
        session_id = uuid4()
        self.user_id_by_session_id[str(session_id)] = user_id
        return str(session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ user_id_for_session_id method
        Returns a session id based on user id
        """
        if session_id is None:
            return None
        if type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user method
        Identifies the current user in session
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """ destroy_session method
        Ends a running session
        """
        if request is None:
            return False
        cookie_session = self.session_cookie(request)
        if cookie_session is None:
            return False
        id_session = self.user_id_for_session_id(cookie_session)
        if id_session is None:
            return False
        del self.user_id_by_session_id[cookie_session]
        return True
