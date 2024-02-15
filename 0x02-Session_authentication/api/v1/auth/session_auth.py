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
    """Session Authentication Class"""

    # Dictionary to map session IDs to user IDs
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a given user ID"""
        if not user_id or not isinstance(user_id, str):
            return None
        # Generate a unique session ID
        session_id = str(uuid.uuid4())
        # Map the session ID to the user ID
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns the user ID associated with a given session ID"""
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current User instance based on the session"""
        # Create a new User instance
        user = User()

        # Get the session ID from the request
        session_id = self.session_cookie(request)
        # Retrieve the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)
        # Get the User object using the user ID
        return user.get(user_id)

    def destroy_session(self, request=None):
        """Destroys the session (logs out the user)"""
        if not request or not self.session_cookie(request):
            return False

        # Get the session ID from the request
        session_id = self.session_cookie(request)
        # Check if session ID exists and associated with a user ID
        if not session_id or not self.user_id_for_session_id(session_id):
            return False
        # Delete the session ID from the dictionary
        del(self.user_id_by_session_id[session_id])
        return True
