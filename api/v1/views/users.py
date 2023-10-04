#!/usr/bin/python3
"""The `users` module"""


from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage


@app_views.route("/users", methods=["GET"], strict_slashes=True)
def list_all_users():
    """Lists all users"""
    user = storage.all("User")
    return jsonify([users.to_dict() for users in user.values()])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=True)
def list_user_id(amenity_id):
    """Lists users by id"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return make_response(jsonify(user.to_dict()), 404)


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=True)
def delete_user(user_id):
    """Deletes user by id"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=True)
def create_user():
    """Creates a new user"""
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    if "email" not in payload:
        abort(400, "Missing email")
    if "password" not in payload:
        abort(400, "Missing password")
    new_user = User(**payload)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=True)
def update_user_id(user_id):
    """Updates user by id"""
    user = storage.get("User", user_id):
        if not user:
            abort(404)
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    for key, value in payload.items():
        if key not in {"id", "email", "created_at", "updated_at"}:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
