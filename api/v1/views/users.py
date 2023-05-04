#!/usr/bin/python3
"""Create a new view for User objects"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/user/all_users.yml', methods=['GET'])
def users():
    """Get all stored users"""
    res = [
        user.to_dict() for user in storage.all(User).values()
    ]
    return jsonify(res)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def user_by_id(user_id):
    """Get a User object by id"""
    res = storage.get(User, user_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """Delete an User object by its id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def insert_user():
    """Insert a new User object"""
    body = request.get_json()
    if type(body) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'email' not in body:
        return abort(400, {'message': 'Missing email'})
    if 'password' not in body:
        return abort(400, {'message': 'Missing password'})
    new_user = User(**body)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def update_user_by_id(user_id):
    """Update an User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    body = request.get_json()
    if type(body) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in body.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
