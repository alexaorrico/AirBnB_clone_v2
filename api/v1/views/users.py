#!/usr/bin/python3
"""users view"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from models.state import State


@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["GET"])
def get_users(user_id=None):
    """retrives the list of all users object of state"""
    list_user = []
    if user_id is None:
        all_objs = storage.all(User).values()
        for v in all_objs:
            list_user.append(v.to_dict())
        return jsonify(list_user)
    else:
        result = storage.get(User, user_id)
        if result is None:
            abort(404)
        return jsonify(result.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_user(user_id):
    """deletes a user object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """create a new post reqs"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400)
    if "name" not in data:
        abort(400, "Missing name")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["PUT"])
def update_user(user_id):
    """updates a amenity object"""
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'email', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
