#!/usr/bin/env python3
"""API authentication module"""

from flask import request
from typing import List, TypeVar
import os


class Auth():
    """Class for managing API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a route requires authorization"""
        if not path or not excluded_paths or not len(excluded_paths):
            return True
        if path[-1] != '/':
            path = path + '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Check if request contains authorization in its header"""
        if not request:
            return None
        if not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user"""
        return None

    def session_cookie(self, request=None):
        """Get the session cookie"""
        if not request:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
