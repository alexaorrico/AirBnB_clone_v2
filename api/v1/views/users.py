#!/usr/bin/python3
"""
module to generate json response
"""

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def all_users():
    """ display all users """
    response = []
    users = storage.all(User)
    for user in users.values():
        response.append(user.to_dict())
    return jsonify(response)


@app_views.route('/users/<user_id>', strict_slashes=False)
def user_by_id(user_id):
    """ display user by id """
    response = storage.get(User, user_id)
    if response is None:
        abort(404)
    return jsonify(response.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id=None):
    """ delete user by id """
    if user_id is None:
        abort(404)
    else:
        trash = storage.get(User, user_id)
        if trash is not None:
            storage.delete(trash)
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ creates a new user """
    try:
        new = request.get_json()
    except Exception:
        pass
    if new is None or type(new) is not dict:
        abort(400, 'Not a JSON')
    if 'email' not in new.keys():
        abort(400, 'Missing email')
    if 'password' not in new.keys():
        abort(400, 'Missing password')
    response = User(**new)
    response.save()
    return make_response(jsonify(response.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """ update an existing user """
    response = storage.get(User, user_id)
    if user_id is None or response is None:
        abort(404)
    try:
        new = request.get_json()
    except Exception:
        pass
    if new is None or type(new) is not dict:
        abort(400, 'Not a JSON')
    for key in new.keys():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(response, key, new[key])
    response.save()
    return make_response(jsonify(response.to_dict()), 200)
