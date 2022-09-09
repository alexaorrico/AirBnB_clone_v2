#!/usr/bin/python3
"""
User instance
"""

from crypt import methods
from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users():
    """
    Retrieves the list of all User objects
    """

    users = []

    for user in storage.all("User").values():
        users.append(user.to_dict())

    return jsonify(users)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def user_by_id(user_id):
    """
    Retrieves the list of all State objects
    """

    user = storage.get("User", user_id)

    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a amenity instance"""

    user = storage.get("User", user_id)

    if user is None:
        abort(404)
    else:
        user.delete(user_id)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a City instance"""
    body = request.get_json()

    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "email" not in body.keys():
        return make_response(jsonify({"error": "Missing email"}), 400)
    elif "password" not in body.keys():
        return make_response(jsonify({"error": "Missing password"}), 400)
    else:
        user = User(**body)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a City instance"""

    body = request.get_json()
    no_update = ["id", "email", "created_at", "updated_at"]

    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    user = storage.get("User", user_id)

    if user is None:
        abort(404)
    
    for key, value in body.items():
        if key not in no_update:
            setattr(user, key, value)
        else:
            pass

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
