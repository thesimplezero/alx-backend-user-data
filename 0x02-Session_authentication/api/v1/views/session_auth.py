#!/usr/bin/env python3
"""
Module of the auth in the views
"""
from flask import jsonify, abort, Flask
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
import os


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_session():
    """POST method
        Return: dictionary representation of the User
    """
    from api.v1.app import auth

    email = request.form.get("email")
    pwd = request.form.get("password")
    session_name = os.getenv("SESSION_NAME")

    if not email or not len(email):
        return jsonify({"error": "email missing"}), 400
    if not pwd or not len(email):
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
    except Exception:
        users = None

    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(pwd):
            try:
                session_id = auth.create_session(user.id)
                user_to_json = jsonify(user.to_json())
                user_to_json.set_cookie(session_name, session_id)
            except Exception:
                break
            return user_to_json
    return jsonify({"error": "wrong password"}), 404


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def logout_session():
    """DELETE method
    Return:
        - empty JSON or 404
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
