#!/usr/bin/python3
'''users file'''
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    '''gets all amenities'''
    users = storage.all(User)
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def req_user(user_id):
    '''gets a specific user'''
    try:
        user = storage.get(User, user_id)
    except KeyError:
        abort(404)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    '''deletes a specific user'''
    try:
        user = storage.get(User, user_id)
    except KeyError:
        abort(404)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    '''post a new user'''
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    email = data.get('email')
    password = data.get('password')
    if email is None:
        abort(400, 'Missing email')
    if password is None:
        abort(400, 'Missing password')
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''updates an existing user'''
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    try:
        user = storage.get(User, user_id)
    except KeyError:
        abort(404)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
