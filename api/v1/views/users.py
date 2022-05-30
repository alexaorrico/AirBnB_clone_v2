#!/usr/bin/python3
"""
Users objects that handles all default RestFul API actions
"""

from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users/", strict_slashes=False)
def get_users():
    """
    Retrieves the list of all Users objects
    """
    users_list = []
    for key, value in storage.all("User").items():
        users_list.append(value.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object
    """
    if storage.get('User', user_id):
        return jsonify(storage.get('User', user_id).to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Delete a User object
    """
    if storage.get('User', user_id):
        storage.delete(storage.get('User', user_id))
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/users/", methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create a User object
    """
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'email' not in request.json:
        abort(400, "Missing email")
    if 'password' not in request.json:
        abort(400, "Missing password")
    _data = request.get_json()
    _status = User(**_data)
    storage.new(_status)
    storage.save()
    _response = jsonify(_status.to_dict())
    _response.status_code = 201
    return _response


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Update a User object
    """
    if not request.is_json:
        abort(400, "Not a JSON")
    if storage.get('User', user_id):
        _data = request.get_json()
        if type(_data) is dict:
            omitir = ['id', 'email', 'created_at', 'updated_at']
            for name, value in _data.items():
                if name not in omitir:
                    setattr(storage.get('User', user_id), name, value)
            storage.save()
            return jsonify(storage.get('User', user_id).to_dict())
    abort(404)
