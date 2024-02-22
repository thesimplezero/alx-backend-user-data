#!/usr/bin/env python3
"""
Flask App
"""

from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def greeting() -> str:
    """Return a greeting on the route /."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """Register a new user."""
    email = request.form.get("email")
    pwd = request.form.get("password")
    try:
        user = AUTH.register_user(email, pwd)
        return jsonify({"email": user.email, "message": "User created"})
    except Exception:
        return jsonify({"message": "Email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
