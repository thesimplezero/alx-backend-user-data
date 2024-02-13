#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module for managing API authentication."""
from flask import request
from typing import List, TypeVar


class Auth(object):
    """Class for managing API authentication."""

    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """Check if authentication is required for a given path."""
        if path is None or excluded_paths is None
        or excluded_paths == []:
            return True

        # Check if the path matches any excluded
        # path with a wildcard at the end
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*') and
            path.startswith(excluded_path[:-1]):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Get the authorization header from the request."""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request."""
        return None
