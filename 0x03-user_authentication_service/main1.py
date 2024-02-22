#!/usr/bin/env python3
"""
Main file
"""

from db import DB
from user import User
from auth import Auth
from flask import Flask, jsonify, request, abort, make_response

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
AUTH = Auth()

# Color codes for better visualization
class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

@app.route("/", methods=['GET'])
def greeting() -> str:
    """Return a greeting."""
    print(f"{bcolors.OKGREEN}Running greeting test...{bcolors.ENDC}")
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """Register a new user."""
    print(f"{bcolors.OKGREEN}Running register_user test...{bcolors.ENDC}")
    email = request.form.get("email")
    pwd = request.form.get("password")
    try:
        user = AUTH.register_user(email, pwd)
        return jsonify({"email": user.email, "message": "User created"})
    except Exception:
        return jsonify({"message": "Email already registered"}), 400

@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login() -> str:
    """Create a session for the user."""
    print(f"{bcolors.OKGREEN}Running login test...{bcolors.ENDC}")
    email = request.form.get("email")
    pwd = request.form.get("password")
    if AUTH.valid_login(email, pwd):
        s_id = AUTH.create_session(email)
        res = make_response({"email": email, "message": "logged in"})
        res.set_cookie("session_id", value=s_id, domain="0.0.0.0", secure=False)
        return res
    else:
        abort(401)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
