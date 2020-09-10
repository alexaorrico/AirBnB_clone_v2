#!/usr/bin/python3
"""Users Api Module"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Return all User objects through the HTTP GET request."""
    all_users = []
    for obj in storage.all(User).values():
        all_users.append(obj.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def users_id_get(user_id):
    """Get a specific User object through the HTTP GET request."""
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)
    return jsonify(obj_user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def user_id_delete(user_id):
    """Delete a specific User object through the HTTP DELETE request."""
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)
    storage.delete(obj_user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """Create a new User object through the HTTP POST request."""
    if not request.get_json(silent=True):
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    if "email" not in req:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in req:
        return make_response(jsonify({"error": "Missing password"}), 400)
    obj_user = User(**req)
    obj_user.save()
    return make_response(jsonify(obj_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def users_id_put(user_id):
    """Update a specific User object through the HTTP PUT request."""
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)
    if not request.get_json(silent=True):
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    for key, value in req.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj_user, key, value)
    obj_user.save()
    return make_response(jsonify(obj_user.to_dict()), 200)
