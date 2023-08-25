#!/usr/bin/python3
"""
new view for User object that handles all default RESTFul API
"""
from models import storage
from models.user import User


from flask import Flask, jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """retrieve a list all users"""
    all_users = []
    users = storage.all("User").values()
    for user in users:
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<string:user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """retrieve a user"""
    all_users = []
    users = storage.all("User").values()
    for user in users:
        all_users.append(user.to_dict())
    for u in all_users:
        if u.get("id") == user_id:
            return jsonify(u)
    abort(404)


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a user"""
    users = storage.all("User")
    try:
        key = 'User.' + user_id
        storage.delete(users[key])
        storage.save()
        return jsonify({}), 200
    except BaseException:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Create a User"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    else:
        request_body = request.get_json()
    if 'email' not in request_body:
        abort(400, 'Missing email')
    elif 'password' not in request_body:
        abort(400, 'Missing password')
    else:
        user = User(**request_body)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a User"""
    users = storage.all(User)
    key = 'User.' + user_id
    try:
        user = users[key]
    except BaseException:
        abort(404)
    if request.is_json:
        request_body = request.get_json()
    else:
        abort(400, 'Not a JSON')
    for key, value in request_body.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
