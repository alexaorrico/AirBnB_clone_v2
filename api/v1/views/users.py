#!/usr/bin/python3
'''
    User route for the API
'''
from flask import Flask
from models import storage
from models.user import User
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/users", methods=["GET"])
def get_users():
    """get user information for all users"""
    users = []
    for users in storage.all(User).values():
        users.append(users.to_dict())
    return jsonify(users)

@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_users_by_id(user_id):
    """get user information for specific users"""
    user = storage.get(User, user_id)
    if user != None:
        return jsonify(user.to_dict())
    else:
        abort(404)

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a user based on its user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return {}

@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_user():
    """ create a user"""
    createJson = request.get_json()
    if createJson is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if not 'name' in createJson.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    user = User(**createJson)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """update a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr is not 'id' or attr is not 'created_at' or attr is not 'updated_at':
            setattr(user, attr, val)
    storage.save()
    return jsonify(user.to_dict())
