#!/usr/bin/python3
"""
view of users
"""
from . import app_views
from flask import jsonify
from models import storage
from models.user import User
from flask import abort, request, Response, make_response
import json


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """
    Retrieves the list of all User objects
    """
    dict_of_users = [obj.to_dict() for obj in storage.all(User).values()]
    response = Response(
        response=json.dumps(dict_of_users, indent=4),
        status=200,
        mimetype='application/json'
    )
    return response


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    """
    Retrieves a User object:
    GET /api/v1/users/<user_id>
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    delete user
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new User object
    """
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json(force=True)
    if 'name' not in data:
        abort(400, 'Missing name')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    updates a new User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json(force=True)
    ignored_keys = ['id', 'updated_at', 'created_at']
    for key, value in data.items():
        if key in ignored_keys:
            continue
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
