#!/usr/bin/env python3
""" Basic Auth module
"""

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ BasicAuth class
    """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """ extract_base64_authorization_header method
        """
        if authorization_header is None:
            return None
        elif type(authorization_header) != str:
            return None
        elif not authorization_header.startswith("Basic "):
            return None
        else:
            header = authorization_header.split()
            return header[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """ decode_base64_authorization_header method
        """
        if base64_authorization_header is None:
            return None
        elif type(base64_authorization_header) != str:
            return None
        try:
            if base64.b64encode(
                base64.b64decode(base64_authorization_header)
            ) == base64_authorization_header:
                return base64_authorization_header
            else:
                content_bytes = base64_authorization_header.encode('utf-8')
                content_string_bytes = base64.b64decode(content_bytes)
                content_string = content_string_bytes.decode('utf-8')
                return content_string
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """ extract_user_credentials method
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        elif type(decoded_base64_authorization_header) != str:
            return (None, None)
        elif ':' not in decoded_base64_authorization_header:
            return (None, None)
        else:
            email = decoded_base64_authorization_header.split(":")[0]
            password = decoded_base64_authorization_header[len(email) + 1:]
            return(email, password)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """ user_object_from_credentials method
        """
        if user_email is None or type(user_email) != str:
            return None
        elif user_pwd is None or type(user_pwd) != str:
            return None
        try:
            user = User.search({"email": user_email})
            if not user or user == []:
                return None
            for u in user:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user method
        """
        header = self.authorization_header(request)
        if header is not None:
            token = self.extract_base64_authorization_header(header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, pwd = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, pwd)
