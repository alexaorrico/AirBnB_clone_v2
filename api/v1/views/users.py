#!/usr/bin/python3
""" Creates API actions for amenities"""

from flask import Flask, abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all amenities"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves amenities based on id"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    result = user.to_dict()
    return jsonify(result)


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes amenity based on id"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def create_user():
    """Creates amenities"""
    data = request.get_json()
    if not data:
        result = {"error": "Not a JSON"}
        return jsonify(result), 400

    email = data.get("email", None)
    if not email:
        result = {"error": "Missing email"}
        return jsonify(result), 400

    password = data.get("password", None)
    if not password:
        result = {"error": "Missing password"}
        return jsonify(result), 400

    new_user = User(**data)
    new_user.save()
    result = new_user.to_dict()
    return jsonify(result), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """Updates amenity based on id"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        result = {"Error": "Not a JSON"}
        return jsonify(result), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, value)

    user.save()
    result = user.to_dict()
    return jsonify(result), 200
