#!/usr/bin/python3
""" Stuff for Users """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """ Return a user """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """ Delete a user """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def add_user():
    """ Add a user """
    if not request.json:
        abort(400, 'Not a JSON')
    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.json:
        abort(400, 'Missing password')
    user = User(**request.json)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201 


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user():
    """ Update a user """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
