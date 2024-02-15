#!/usr/bin/env python3
"""
Session Authentication Module
"""
from api.v1.auth.auth import Auth
from flask import request
from models.user import User
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """Auth class Session
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID
        """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a session id by user id
        """
        if not session_id and not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns current User instance
        """
        user = User()

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return user.get(user_id)

    def destroy_session(self, request=None):
        """Log out session
        """
        if not request or not self.session_cookie(request):
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        del(self.user_id_by_session_id[session_id])
        return True
