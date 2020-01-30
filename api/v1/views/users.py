#!/usr/bin/python3
""" States Module"""


from models.user import User
from models import storage
from flask import Flask, abort, jsonify, request, json
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """    Retrieves the list of all Users objects
    """
    users = []
    for key, value in storage.all("User").items():
        users.append(value.to_dict())
    return jsonify(users)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object by id
    """
    user = storage.get("User", user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create a new User instance
    """
    if request.is_json:
        dicc = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' in dicc:
        new_user = User()
        new_user.name = dicc["name"]
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201
    else:
        return jsonify({"error": "Missing name"}), 400


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Update a User instance
    """
    if not request.json:
        abort(400, "Not a JSON")
    user = storage.get("User", id=user_id)
    if user:
        user.name = request.json['name']
        user.save()
        return jsonify(user.to_dict()), 200
    abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Delete a User instance
    """
    user = storage.get("User", id=user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)
