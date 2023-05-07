#!/usr/bin/python3
'''BLueprint implementation for user model'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_users(user_id=None):
    '''Return the list of all User objects'''
    if request.method == 'DELETE':
        return del_user(user_id)
    elif request.method == 'POST':
        return add_user()
    elif request.method == 'PUT':
        return update_user(user_id)
    elif request.method == 'GET':
        return get_users(user_id)


def get_users(user_id=None):
    '''Handles all get request to users endpoint'''
    if user_id:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())
    users_k = [val.to_dict() for val in storage.all(User).values()]
    return jsonify(users_k)


def del_user(user_id):
    '''Deletes a user obj with user_id'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


def add_user():
    '''Adds user to users'''
    try:
        req_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if type(req_data) is not dict:
        abort(400, 'Not a JSON')
    if 'email' not in req_data:
        abort(400, 'Missing email')
    if 'password' not in req_data:
        abort(400, 'Missing password')
    user = User(**req_data)
    user.save()
    return get_users(user.id), 201


def update_user(user_id):
    '''Update a user instance'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    try:
        req_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if type(req_data) is not dict:
        abort(400, 'Not a JSON')
    for key, val in req_data.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(user, key, val)
    user.save()
    return get_users(user.id), 200
