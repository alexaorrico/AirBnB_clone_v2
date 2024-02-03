#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, request, jsonify


@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["GET"])
def user(user_id=None):
    """show user and user with id"""
    user_list = []
    if user_id is None:
        all_objs = storage.all(User).values()
        for v in all_objs:
            user_list.append(v.to_dict())
        return jsonify(user_list)
    else:
        result = storage.get(User, user_id)
        if result is None:
            abort(404)
        return jsonify(result.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["DELETE"])
def user_delete(user_id):
    """delete method"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """creates a new post req"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
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
    """update user"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.password = data.get("password", obj.password)
    obj.first_name = data.get("first_name", obj.first_name)
    obj.last_name = data.get("last_name", obj.last_name)
    obj.save()
    return jsonify(obj.to_dict()), 200