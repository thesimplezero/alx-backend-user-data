#!/usr/bin/env python3
"""Basic authentication
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """A Basic Authentication class
    """
    def extract_base64_authorization_header(self, auth_h: str) -> str:
        """Returns the Base64 of the Authorization header
        """
        if not auth_h or not isinstance(auth_h, str) or \
           not auth_h.startswith("Basic "):
            return None
        return auth_h[6:]

    def decode_base64_authorization_header(self, b64_auth_h: str) -> str:
        """Returns the decoded value of a Base64 string
        b64_auth_h
        """
        if not b64_auth_h or not isinstance(b64_auth_h, str):
            return None
        try:
            b = base64.b64decode(b64_auth_h)
            decoded = b.decode("utf-8")
        except Exception:
            return None
        return decoded

    def extract_user_credentials(self, decoded_b64_auth_h: str) -> (str, str):
        """Returns the user email and password from the Base64
        decoded value.
        """
        if not decoded_b64_auth_h or \
           not isinstance(decoded_b64_auth_h, str) or \
           ':' not in decoded_b64_auth_h:
            return (None, None)
        credentials = decoded_b64_auth_h.split(":", 1)
        return (credentials[0], credentials[1])

    def user_object_from_credentials(self, e: str, p: str) -> TypeVar('User'):
        """Retrieves a User instance based on email
        and password
        """
        if not e or not p or \
           not isinstance(e, str) or not isinstance(p, str):
            return None
        try:
            user = User.search({"email": e})
        except Exception:
            return None
        if user:
            for u in user:
                if u.is_valid_password(p):
                    return u
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request
        """
        try:
            header = self.authorization_header(request)
            base64 = self.extract_base64_authorization_header(header)
            decoded = self.decode_base64_authorization_header(base64)
            cred = self.extract_user_credentials(decoded)
            user = self.user_object_from_credentials(cred[0], cred[1])
            return user
        except Exception:
            return None
