#!/usr/bin/python3
"""Users hanlders."""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieve all the users."""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route(
    "/users/<string:user_id>", methods=["GET"], strict_slashes=False
)
def get_user(user_id):
    """Get info about specified user."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
    "/users/<string:user_id>", methods=["DELETE"], strict_slashes=False
)
def delete_user(user_id):
    """Delete specified user."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Create a new user."""
    req = request.get_json(silent=True)
    if not req:
        abort(400, "Not a JSON")
    if "email" not in req:
        abort(400, "Missing email")
    if "password" not in req:
        abort(400, "Missing passord")
    user = User(**req)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route(
    "/users/<string:user_id>", methods=["PUT"], strict_slashes=False
)
def update_user(user_id):
    """Update specified user."""
    req = request.get_json(silent=True)
    if not req:
        abort(400, "Not a JSON")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for attr, val in request.get_json().items():
        if attr not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, attr, val)
    user.save()
    return jsonify(user.to_dict())
