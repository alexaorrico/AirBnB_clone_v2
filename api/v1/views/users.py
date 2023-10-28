#!/usr/bin/python3
""" holds class User"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'])
def get_users():
    """ Retrieves the list of all User objects """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'])
def post_user():
    """ Creates a User """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """ Updates a User object """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore = ['id', 'email', 'created_at', 'updated_at']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
