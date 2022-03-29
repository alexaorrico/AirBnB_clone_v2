#!/usr/bin/python3
""" API view for User objects. """
from api.v1.views import app_views
from flask import jsonify, request, abort
import json
from models import storage
from models.user import User
import os


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def all_users(text="is_cool"):
    """ Returns list of all User objs. """
    users = list(storage.all(User).values())
    list_users = []
    for user in users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """ Returns the User obj in JSON. """
    try:
        user = storage.all(User)["User.{}".format(user_id)]
    except (TypeError, KeyError):
        abort(404)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """ Deletes the User obj from Storage. """
    try:
        user = storage.all(User)["User.{}".format(user_id)]
    except (TypeError, KeyError):
        abort(404)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user(text="is_cool"):
    """ Creates a new User and saves to Storage. """
    content = request.get_json()
    try:
        json.dumps(content)
        if 'email' not in content:
            abort(400, {'message': 'Missing email'})
        if 'password' not in content:
            abort(400, {'message': 'Missing password'})
    except (TypeError, OverflowError):
        abort(400, {'message': 'Not a JSON'})
    new_user = User(**content)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """ Updates a User obj and saves to Storage. """
    try:
        user = storage.all(User)["User.{}".format(user_id)]
    except (TypeError, KeyError):
        abort(404)
    if not user:
        abort(404)
    content = request.get_json()
    try:
        json.dumps(content)
    except (TypeError, OverflowError):
        abort(400, {'message': 'Not a JSON'})
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in content.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
