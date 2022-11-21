#!/usr/bin/python3
""" This script provides views of Amenity """

from flask import abort, jsonify, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves a list of all user objects"""
    data = [
        user.to_dict() for user in storage.all(User).values()
    ]
    return jsonify(data)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a user object"""
    res = storage.get(User, user_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Creates a user object"""
    body = request.get_json()
    if type(body) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'email' not in body:
        return abort(400, {'message': 'Missing email'})
    if 'password' not in body:
        return abort(400, {'message': 'Missing password'})
    n_user = User(**body)
    n_user.save()
    return jsonify(n_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                methods=['PUT'])
def update_user(user_id):
    """Updates a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    body = request.get_json()
    if type(body) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for k, v in body.items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200
