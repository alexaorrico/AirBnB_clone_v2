#!/usr/bin/python3
"""This view implements the RESTFul operations for `User` objects"""
from flask import jsonify, request, abort, make_response
from . import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def read_users(user_id=None):
    """Returns a JSON list of all `User` objects"""
    if user_id is None:
        return jsonify([user.to_dict() for user in storage.all(User).values()])

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/', methods=['POST'])
def create_user():
    """Creates a new `User` object"""
    user_data = request.get_json(silent=True)
    if user_data is None:
        abort(400, "Not a JSON")
    if "email" not in user_data:
        abort(400, "Missing email")
    if "password" not in user_data:
        abort(400, "Missing password")

    email = user_data.get("email")
    password = user_data.get("password")
    first_name = user_data.get("first_name", None)
    last_name = user_data.get("last_name", None)

    new_user = User(email=email, password=password,
                    first_name=first_name, last_name=last_name)
    new_user.save()

    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update data for a given user"""

    user_data = request.get_json(silent=True)
    if user_data is None:
        abort(400, "Not a JSON")

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    allowed = ["password", "first_name", "last_name"]

    for key, value in user_data.items():
        if key in allowed:
            setattr(user, key, value)

    user.save()
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a given user from storage"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()

    return make_response(jsonify({}), 200)
