#!/usr/bin/python3
""" Users file """

import models
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/users')
def get_users():
    """
    Retrieves the list of all User objects
    """
    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>')
def get_user(user_id):
    """
    Retrieves an User instance
    """
    user = storage.get("User", id=user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """
    Create a new User instance
    """
    if not request.json:
        abort(400, "Not a JSON")
    if 'email' not in request.json:
        abort(400, "Missing email")
    if 'password' not in request.json:
        abort(400, "Missing password")
    user = models.user.User(**request.json)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update a User instance
    """
    if not request.json:
        abort(400, "Not a JSON")
    user = storage.get("User", user_id)
    if user:
        if 'password' in request.json.keys():
            user.password = request.json['password']
        if 'first_name' in request.json.keys():
            user.first_name = request.json['first_name']
        if 'last_name' in request.json.keys():
            user.last_name = request.json['last_name']
        user.save()
        return jsonify(user.to_dict()), 200
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user instance
    """
    user = storage.get("User", user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)
