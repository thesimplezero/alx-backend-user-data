#!/usr/bin/env python3
"""Basic authentication module"""

from flask import request
from typing import TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication Class"""

    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """Extracts Base64 from the Authorization header"""
        if not auth_header or not isinstance(auth_header, str) or \
                not auth_header.startswith("Basic "):
            return None
        return auth_header[6:]

    def decode_base64_authorization_header(self, b64_auth_header: str) -> str:
        """Decodes a Base64 string"""
        if not b64_auth_header or not isinstance(b64_auth_header, str):
            return None
        try:
            decoded = base64.b64decode(b64_auth_header).decode("utf-8")
        except Exception:
            return None
        return decoded

    def extract_user_credentials(self, decoded_b64_auth_header: str) -> (str, str):
        """Extracts user credentials from a decoded Base64 string"""
        if not decoded_b64_auth_header or \
                not isinstance(decoded_b64_auth_header, str) or \
                ':' not in decoded_b64_auth_header:
            return (None, None)
        return tuple(decoded_b64_auth_header.split(":", 1))

    def user_object_from_credentials(self, email: str,
                                     password: str) -> TypeVar('User'):
        """Retrieves a User instance based on email and password"""
        if not email or not password or \
                not isinstance(email, str) or not isinstance(password, str):
            return None
        try:
            users = User.search({"email": email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(password):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request"""
        try:
            auth_header = self.authorization_header(request)
            base64_auth = self.extract_base64_authorization_header(auth_header)
            decoded_auth = self.decode_base64_authorization_header(base64_auth)
            email, password = self.extract_user_credentials(decoded_auth)
            return self.user_object_from_credentials(email, password)
        except Exception:
            return None
