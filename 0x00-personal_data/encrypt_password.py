#!/usr/bin/env python3

""" Hashing Passwords """

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt."""
    encoded_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(encoded_password, salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a password is valid."""
    encoded_password = password.encode('utf-8')
    return bcrypt.checkpw(encoded_password, hashed_password)
