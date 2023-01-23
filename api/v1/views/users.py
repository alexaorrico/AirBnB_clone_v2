#!/usr/bin/python3
"""
users view routes
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route(
    "/users",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def users():
    """Handles /users endpoint

    Returns:
        json: list of all users or the newly added user
    """
    if request.method == "POST":
        user_data = request.get_json(silent=True)
        if user_data is None:
            return jsonify(error="Not a JSON"), 400

        if "email" not in user_data:
            return jsonify(error="Missing email"), 400
        elif "password" not in user_data:
            return jsonify(error="Missing password"), 400
        else:
            user = User(**user_data)
            storage.new(user)
            storage.save()
            return jsonify(user.to_dict()), 201

    else:
        users = list(storage.all(User).values())
        return jsonify([user.to_dict() for user in users])


@app_views.route(
    "/users/<user_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def user(user_id=None):
    """Handles /users/user_id endpoint

    Returns:
        json: object for GET, empty dict for DELETE or 404
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({})
    elif request.method == "PUT":
        user_data = request.get_json(silent=True)
        if user_data is None:
            return jsonify(error="Not a JSON"), 400

        for key, value in user_data.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict())

    else:
        return jsonify(user.to_dict())
