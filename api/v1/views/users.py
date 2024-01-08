#!/usr/bin/python3
""""view for Users objects that handles all RESTFul API actions"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users")
@app_views.route("/users/<user_id>", methods=["GET"])
def get_users(user_id=None):
    """retreive the list of all Users or a user with user_id"""
    if user_id is None:
        users = storage.all(User).values()
        return make_response(jsonify([user.to_dict() for user in users]), 200)

    user = storage.get("User", user_id)
    if user:
        return make_response(jsonify(user.to_dict()), 200)

    abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id=None):
    """remove user from storage"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    user.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"])
def create_user():
    """create a new"""
    user_data = request.get_json(silent=True)

    print(user_data)
    if user_data is None:
        abort(400, "Not a JSON")
    if "email" not in user_data:
        abort(400, "Missing email")
    if "password" not in user_data:
        abort(400, "Missing password")
    user = User(email=user_data["email"], password=user_data["password"])
    user.save()
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id=None):
    """update user information"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user_data = request.get_json(silent=True)
    if user_data is None:
        abort(400, "Not a JSON")

    ignore_attr = ["id", "updated_at", "created_at", "email"]
    [setattr(user, attr, user_data[attr])
     for attr in user_data if attr not in ignore_attr]

    storage.save()
    return jsonify(user.to_dict())
