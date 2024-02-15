#!/usr/bin/env python3
"""
Authentication Module for API Views
"""

from flask import jsonify, abort, request, jsonify, Flask
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth
import os

SESSION_NAME = os.getenv("SESSION_NAME")


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_session():
    """POST method for user login"""
    email = request.form.get("email")
    pwd = request.form.get("password")

    if not email or not pwd:
        return jsonify({"error": "email or password missing"}), 400

    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(pwd):
            try:
                session_id = auth.create_session(user.id)
                user_to_json = jsonify(user.to_json())
                user_to_json.set_cookie(SESSION_NAME, session_id)
                return user_to_json
            except Exception:
                break

    return jsonify({"error": "wrong email or password"}), 404


@app_views.route("/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout_session():
    """DELETE method for user logout"""
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
