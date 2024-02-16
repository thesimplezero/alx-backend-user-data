#!/usr/bin/env python3
"""Defines user-related API views."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users - Return list of all User objects."""
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """GET /api/v1/users/:id - Return User object JSON."""
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/:id - Delete User by ID."""
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users/ - Create a new User."""
    rj = request.get_json()
    if not rj or not isinstance(rj, dict):
        return jsonify({'error': 'Wrong format'}), 400
    if not rj.get('email') or not rj.get('password'):
        return jsonify({'error': 'email or password missing'}), 400
    try:
        user = User(**rj)
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/:id - Update User by ID."""
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    rj = request.get_json()
    if not rj or not isinstance(rj, dict):
        return jsonify({'error': 'Wrong format'}), 400
    user.update(rj)
    user.save()
    return jsonify(user.to_json()), 200
