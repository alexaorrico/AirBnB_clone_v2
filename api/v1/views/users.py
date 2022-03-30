#!/usr/bin/python3
"""
Create a new view for User object that
handles all default RESTFul API actions
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask.json import jsonify
from flask import abort
from flask import request

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects
    """
    users = storage.all(User)
    info = []
    for user in users.values():
        info.append(user.to_dict())
    return jsonify(info)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_one_user(user_id=None):
    """
    Retrieves a User object
    """
    user = storage.get(User, user_id)
    if user is not None:
        return jsonify(user.to_dict())
    abort(404)

@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a User object:
    """
    user = storage.get(User, user_id)
    if user is not None:
        user.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)

@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """
    Creates a User
    """
    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")
    if 'password' not in json:
        abort(400, 'Missing password')
    if 'email' not in json:
        abort(400, 'Missing email')
    user = User(**json)
    user.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """
    Updates a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")
    for key, value in json.items():
        if key != 'updated_at' and key != 'created_at' and key != 'id' and key != 'email':
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
