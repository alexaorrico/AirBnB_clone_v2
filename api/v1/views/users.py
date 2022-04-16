#!/usr/bin/python3
"""Users"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route("/users",
                 methods=['GET'],
                 strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects: GET /api/v1/users"""
    list = []
    user_obj = storage.all(User).values()
    for a in user_obj:
        list.append(a.to_dict())
    return jsonify(list)


@app_views.route("/users/<user_id>",
                 methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object: GET /api/v1/users/<user_id>"""
    user_obj = storage.get(User, user_id)
    if user_obj:
        return jsonify(user_obj.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_users(user_id):
    """Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>"""
    user_obj = storage.get(User, user_id)
    if user_obj:
        storage.delete(user_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users",
                 methods=['POST'],
                 strict_slashes=False)
def create_users():
    """Creates a User: POST /api/v1/users"""
    obj_request = request.get_json()
    if obj_request:
        if 'email' not in obj_request.keys():
            return "Missing email", 400
        if 'password' not in obj_request.keys():
            return "Missing password", 400

        new_user_obj = User(**obj_request)
        storage.new(new_user_obj)
        storage.save()
        current_state = storage.get(User, new_user_obj.id)
        return jsonify(current_state.to_dict()), 201
    else:
        return "Not a JSON", 400


@app_views.route("/users/<user_id>",
                 methods=['PUT'],
                 strict_slashes=False)
def updates_users(user_id):
    """Updates a User object: PUT /api/v1/users/<user_id>"""
    user_obj = storage.get(User, user_id)
    obj_request = request.get_json()
    if user_obj:
        if obj_request:
            for key, value in obj_request.items():
                ignore = ["id", "email", "created_at", "updated_at"]
                if key not in ignore:
                    setattr(user_obj, key, value)
            storage.save()
            return (jsonify(user_obj.to_dict()), 200)
        else:
            return "Not a JSON", 400
    else:
        abort(404)
