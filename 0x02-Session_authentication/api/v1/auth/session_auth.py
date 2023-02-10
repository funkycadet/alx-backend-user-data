#!/usr/bin/env python3
""" Session Authentication module
"""
from .auth import Auth
import uuid


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
        elif type(user_id) != str:
            return None
        else:
            session_id = uuid.uuid4()
            print(session_id)
            self.user_id_by_session_id[session_id] = user_id
            return session_id
