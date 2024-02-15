#!/usr/bin/env python3
"""User Views Module"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users
    Returns:
      - JSON representation of a list containing all User objects
    """
    # Retrieve all User objects and convert them to JSON format
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """GET /api/v1/users/:id
    Path parameters:
      - user_id: User ID
    Returns:
      - JSON representation of a single User object
      - 404 if the User ID doesn't exist
    """
    # Check if user_id is provided
    if user_id is None:
        abort(404)
    # Special case handling for 'me' route
    if user_id == "me":
        # If current user is not available, return 404
        if not request.current_user:
            abort(404)
        return jsonify(request.current_user.to_json())
    # Retrieve the User object with the provided ID
    user = User.get(user_id)
    # If user doesn't exist, return 404
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/:id
    Path parameters:
      - user_id: User ID
    Returns:
      - Empty JSON if the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    # Check if user_id is provided
    if user_id is None:
        abort(404)
    # Retrieve the User object with the provided ID
    user = User.get(user_id)
    # If user doesn't exist, return 404
    if user is None:
        abort(404)
    # Remove the user
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Returns:
      - JSON representation of the created User object
      - 400 if unable to create the new User
    """
    # Initialize variables
    rj = None
    error_msg = None
    try:
        # Attempt to parse JSON from request body
        rj = request.get_json()
    except Exception as e:
        rj = None
    # Check if JSON is not None
    if rj is None:
        error_msg = "Wrong format"
    # Check if email is missing
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"
    # Check if password is missing
    if error_msg is None and rj.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            # Create a new User object
            user = User()
            user.email = rj.get("email")
            user.password = rj.get("password")
            user.first_name = rj.get("first_name")
            user.last_name = rj.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/:id
    Path parameters:
      - user_id: User ID
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Returns:
      - JSON representation of the updated User object
      - 404 if the User ID doesn't exist
      - 400 if unable to update the User
    """
    # Check if user_id is provided
    if user_id is None:
        abort(404)
    # Retrieve the User object with the provided ID
    user = User.get(user_id)
    # If user doesn't exist, return 404
    if user is None:
        abort(404)
    rj = None
    try:
        # Attempt to parse JSON from request body
        rj = request.get_json()
    except Exception as e:
        rj = None
    # Check if JSON is None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    # Update user's first_name if provided
    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    # Update user's last_name if provided
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')
    # Save the changes
    user.save()
    return jsonify(user.to_json()), 200
