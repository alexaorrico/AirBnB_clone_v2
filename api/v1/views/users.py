#!/usr/bin/python3
"""Create a new view for User object that handles all default RestFul API"""


from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    userList = []
    users = storage.all('User')
    for user in users.values():
        userList.append(user.to_dict())
    return jsonify(userList)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['GET'])
def get_user(user_id):
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    else:
        return(jsonify(user.to_dict()))


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Creates a User"""
    res = request.get_json()
    if res is None:
        abort(400, "Not a JSON")
    if 'email' not in res:
        abort(400, "Missing email")
    if 'password' not in res:
        abort(400, "Missing password")
    newUser = User(**res)
    storage.new(newUser)
    storage.save()
    return jsonify(newUser.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def modify_user(user_id):
    res = request.get_json()
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    if res is None:
        abort(400, 'Not a JSON')
    for k, v in res.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200
