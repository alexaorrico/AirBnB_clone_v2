#!/usr/bin/python3
"""
Handles HTTP requests for User objects
"""

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def list_users():
    """ Retrieve and return a list of all User objects """
    response = []
    users = storage.all(User)
    for user in users.values():
        response.append(user.to_dict())
    return jsonify(response)


@app_views.route('/users/<user_id>', strict_slashes=False)
def retrieve_user(user_id):
    """ Fetch and return a specific User object by its ID """
    response = storage.get(User, user_id)
    if response is None:
        abort(404)
    return jsonify(response.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def remove_user(user_id=None):
    """ Remove a User object by its ID """
    if user_id is None:
        abort(404)
    else:
        user = storage.get(User, user_id)
        if user is not None:
            storage.delete(user)
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """ Create a new User object """
    try:
        new_data = request.get_json()
    except Exception:
        pass
    if new_data is None or type(new_data) is not dict:
        abort(400, 'Not a JSON')
    if 'email' not in new_data:
        abort(400, 'Missing email')
    if 'password' not in new_data:
        abort(400, 'Missing password')
    user = User(**new_data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def modify_user(user_id=None):
    """ Update an existing User object by its ID """
    user = storage.get(User, user_id)
    if user_id is None or user is None:
        abort(404)
    try:
        update_data = request.get_json()
    except Exception:
        pass
    if update_data is None or type(update_data) is not dict:
        abort(400, 'Not a JSON')
    for key in update_data.keys():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, update_data[key])
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
