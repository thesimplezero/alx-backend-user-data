#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Implement basic auth
"""

import base64
import binascii
from typing import TypeVar

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """implement basic auth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract base64 authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) -> str:
        """Decode a Base64-encoded string
        """
        if type(base64_authorization_header) == str:
            try:
                res = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return res.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """extract user credentials
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """user object from credentials
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        extract_base64 = self.extract_base64_authorization_header(auth_header)
        if extract_base64 is None:
            return None
        decode_base64 = self.decode_base64_authorization_header(extract_base64)
        if decode_base64 is None:
            return None
        user_credentials = self.extract_user_credentials(decode_base64)
        if user_credentials is None:
            return None
        user_object = self.user_object_from_credentials(
            user_credentials[0], user_credentials[1])
        return user_object
