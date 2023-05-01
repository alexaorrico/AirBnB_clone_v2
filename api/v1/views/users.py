#!/usr/bin/python3

'''
This module creates views for the users class
Routes:
    GET /users - Returns a list of all users in the database
    GET /users/<user_id> - Returns a user object based on the user_id
    DELETE /users/<user_id> - Deletes a user object based on the user_id
    POST /users - Creates a new user based on the JSON object passed
    PUT /users/<user_id> - Updates a user object based on JSON object passed
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''
    Retrieves a list of users in the database
    '''
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    '''
    Retrieves a user object based on the user_id
    '''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''
    Deletes a user object
    '''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''
    Creates a new user
    '''
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if 'email' not in body:
        abort(400, 'Missing email')
    if 'password' not in body:
        abort(400, 'Missing password')
    user = User(**body)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''
    Updates a user
    '''
    user = storage.get(User, user_id)
    body = request.get_json()
    if user is None:
        abort(404)
    if body is None:
        abort(400, 'Not a JSON')
    for k, v in body.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200
