#!/usr/bin/python3
"""user route"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """get a list of users"""
    users = [obj.to_dict() for obj in storage.all(User).values()]
    return make_response(jsonify(users), 200)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """get user by id"""
    user = storage.get(User, user_id)
    return make_response(jsonify(user.to_dict()),
                         200) if user else abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """create a new user"""
    user = request.get_json()
    if not user:
        return make_response("Not a JSON", 400)
    if not user.get('email'):
        return make_response("Missing email", 400)
    if not user.get('password'):
        return make_response("Missing password", 400)
    new_user = User(**user)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """update a user by id"""
    cur_user = storage.get(User, user_id)
    if not cur_user:
        abort(404)
    new_user = request.get_json()
    if not new_user:
        return make_response("Not a JSON", 400)
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in new_user.items():
        if key not in ignored_keys:
            setattr(cur_user, key, value)
    storage.save()
    return make_response(cur_user.to_dict(), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """delete user by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response({}, 200)
