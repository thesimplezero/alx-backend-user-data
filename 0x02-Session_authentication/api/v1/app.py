#!/usr/bin/env python3
"""
Route module for the API
"""

# Import necessary modules
import os
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

# Import API views
from api.v1.views import app_views

# Initialize Flask app
app = Flask(__name__)

# Register API blueprints
app.register_blueprint(app_views)

# Enable CORS for all routes
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Determine authentication type based on environment variable
auth = None
auth_type = os.getenv("AUTH_TYPE")
if auth_type == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


# Error handling for 404 - Not Found
@app.errorhandler(404)
def not_found(error) -> str:
    """Handler for 404 Not Found errors"""
    return jsonify({"error": "Not found"}), 404


# Error handling for 401 - Unauthorized
@app.errorhandler(401)
def not_authorized(error) -> str:
    """Handler for 401 Unauthorized errors"""
    return jsonify({"error": "Unauthorized"}), 401


# Error handling for 403 - Forbidden
@app.errorhandler(403)
def forbidden(error) -> str:
    """Handler for 403 Forbidden errors"""
    return jsonify({"error": "Forbidden"}), 403


# Filter requests before processing
@app.before_request
def before_request():
    """Filtering requests"""
    needs_auth = ['/api/v1/status/',
                  '/api/v1/unauthorized/',
                  '/api/v1/forbidden/',
                  '/api/v1/auth_session/login/'
                  ]
    if auth:
        if not auth.require_auth(request.path, needs_auth):
            return
        if (not auth.authorization_header(request) and
                not auth.session_cookie(request)):
            abort(401)
        if not auth.current_user(request):
            abort(403)
    request.current_user = auth.current_user(request)


# Entry point of the application
if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
