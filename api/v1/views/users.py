#!/usr/bin/python3
"""Create a new view for User object that handles all default RestFul API"""


from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def user():
    """Retrieves the list of all User objects"""
    users = storage.all('User')
    list_user = []
    for x in users.values():
        list_user.append(x.to_dict())
    return jsonify(list_user)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def users_id(user_id=None):
    """Retrieves a User object"""
    users = storage.get('User', user_id)
    if users is None:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """Deletes a User object"""
    users = storage.get('User', user_id)
    if users is None:
        abort(404)
    storage.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
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


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id=None):
    """Updates a User object"""
    users = storage.get('User', user_id)
    res = request.get_json()

    if users is None:
        abort(404)
    if res is None:
        abort(404, "Not a JSON")
    for k, v in res.items():
        if k != 'id' and k != 'email' and \
           k != 'updated_at' and k != 'created_at':
            setattr(users, k, v)
    storage.save()
    return jsonify(users.to_dict()), 200
