#!/usr/bin/python3
"""
API User View Module

Defines the API views for user objects, providing RESTful
endpoints to interact with user resources.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_list_users():
    """ Gets a list of all User objects """
    users_list = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_id(user_id):
    """ Gets a User object by its ID """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_id(user_id):
    """ Deletes a User object by its ID """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    """ Creates a User object """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")

    new_user = User(email=data["email"], password=data["password"])
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def updates_user(user_id):
    """ Updates a User object by its ID """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "first_name" in data:
        user.first_name = data["first_name"]
    if "last_name" in data:
        user.last_name = data["last_name"]
    storage.save()
    return jsonify(user.to_dict()), 200
