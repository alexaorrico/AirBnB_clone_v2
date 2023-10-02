#!/usr/bin/python3
"""User objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all("User").values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves, Deletes or Updates a User object by it's id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    if request.method == "GET":
        return jsonify(user.to_dict())

    elif request.method == "DELETE":
        user.delete()
        storage.save()
        return jsonify({}), 200

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if "email" not in data:
        return "Missing email", 400
    if "password" not in data:
        return "Missing password", 400
    nope = {"id", "email", "created_at", "updated_at"}
    [setattr(user, key, val) for key, val in data.items() if key not in nope]
    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object"""
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if "email" not in data:
        return "Missing email", 400
    if "password" not in data:
        return "Missing password", 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201
