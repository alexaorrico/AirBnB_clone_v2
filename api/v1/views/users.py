#!/usr/bin/python3
"""RESTful API actions for User objects"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def get_users():
    users = [user.to_dict() for user in storage.all(User).values()]

    return jsonify(users)


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    data = request.get_json()

    if not data:
        abort(404, "Not a JSON")
    if "email" not in data:
        abort(404, "Missing email")
    if "password" not in data:
        abort(404, "Missing password")

    new_user = User(**data)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)

    if user:
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")

        ignore_keys = ["id", "email", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
