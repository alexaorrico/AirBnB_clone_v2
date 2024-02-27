#!/usr/bin/python3
"""
view for User object that handles all default RESTFul API actions
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    all_users = storage.all("User").values()
    result = [user.to_dict() for user in all_users]
    return jsonify(result.to_dict), 200


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get("User", str(user_id))
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get("User", str(user_id))
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return ({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a user"""
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, "Not a JSON")
    if "email" not in user_json:
        abort(400, "Missing email")
    if "password" not in user_json:
        abort(400, "Missing password")
    user_inst = User(**user_json)
    user_inst.save()
    return jsonify(user_inst.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user_obj = storage.get("User", str(user_id))
    if user_obj is None:
        abort(404)
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, "Not a JSON")
    for key, val in user_json.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user_obj, key, val)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
