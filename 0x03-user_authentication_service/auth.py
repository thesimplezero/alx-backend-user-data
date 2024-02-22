#!/usr/bin/env python3
"""Authentication module"""
import bcrypt
import uuid
from typing import TypeVar
from db import DB
from user import User

class Auth:
    """Authentication class that manages user authentication."""

    def __init__(self):
        """Initialize Auth with database connection."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except ValueError:
            raise
        except Exception:
            hashed_pwd = self._hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials."""
        try:
            user = self._db.find_user_by(email=email)
            password = password.encode("utf-8")
            return bcrypt.checkpw(password, user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """Create a session for the user."""
        user = self._db.find_user_by(email=email)
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """Retrieve user using session ID."""
        try:
            if not session_id:
                return None
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy user session."""
        try:
            self._db.update_user(user_id=user_id, session_id=None)
            return None
        except Exception:
            raise

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token."""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password using reset token."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = self._hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_pwd,
                                 reset_token=None)
            return None
        except Exception:
            raise ValueError

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash the provided password."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def _generate_uuid() -> str:
        """Generate a UUID."""
        return str(uuid.uuid1())
