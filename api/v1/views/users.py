#!/usr/bin/python3
""" Routes for handling User objects """
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """ Retrieves all User objects """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    """ Retrieves a specific User object by ID """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user_by_id(user_id):
    """ Deletes a User object by ID """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """ Creates a new User """
    user_json = request.get_json()
    if not user_json:
        abort(400, 'Not a JSON')
    if "email" not in user_json:
        abort(400, 'Missing email')
    if "password" not in user_json:
        abort(400, 'Missing password')

    new_user = User(**user_json)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object by ID """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user_json = request.get_json()
    if not user_json:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in user_json.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()

    return jsonify(user.to_dict()), 200
