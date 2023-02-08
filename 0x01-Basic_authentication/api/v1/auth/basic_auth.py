#!/usr/bin/env python3
""" Basic Auth module
"""

from api.v1.auth.auth import Auth
import base64


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
            if base64.b64encode(base64.b64decode(base64_authorization_header)) == base64_authorization_header:
                return base64_authorization_header
            else:
                content_bytes = base64_authorization_header.encode('utf-8')
                content_string_bytes = base64.b64decode(content_bytes)
                content_string = content_string_bytes.decode('utf-8')
                return content_string
        except Exception:
            return None
