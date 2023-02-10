#!/usr/bin/env python3
""" Session Authentication module
"""
from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ SessionAuth class
    """
    user_id_by_session_id = {}

    def __init__(self):
        """ __init__ method
        """
        pass

    def create_session(self, user_id: str = None) -> str:
        """ create_session method
        This method creates a new session for users
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
        """
        if session_id is None:
            return None
        if type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)
