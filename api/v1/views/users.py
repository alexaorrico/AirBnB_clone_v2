#!/usr/bin/python3
"""
View for Users objects that handles
all default RestFul API actions.
"""

from flask import Flask, render_template
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
import models


@app_views.route('/users', methods=['GET'])
def all_users():
    """Retrieves the list of all User objects"""
    all_users = storage.all('User').values()
    list_users = []

    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def user_id(user_id):
    """Retrieves the list of a specific user"""
    user = storage.get('User', user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def user_delete(user_id):
    """Deletes an Amenity"""
    user = storage.get('User', user_id)
    if user:
        user.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def amenity_post():
    """Creates an user"""
    if not request.get_json():
        return jsonify({'message': 'Not a JSON'}), 400
    if 'email' not in request.get_json():
        return jsonify({'message': 'Missing email'}), 400
    if 'password' not in request.get_json():
        return jsonify({'message': 'Missing password'}), 400

    user = user.User(name=request.get_json().get('name'))
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def user_put(user_id):
    """Updates an user"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    for k, v in request.get_json().items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict())
