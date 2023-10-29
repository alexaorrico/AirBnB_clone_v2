#!/usr/bin/python3
"""state view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """retrieve all users"""
    users_list = []
    for user in storage.all(User).values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def a_user(user_id):
    """retrieve a user with its id"""
    try:
        user = storage.get(User, user_id)
        return jsonify(user.to_dict())
    except Exception:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a State object"""
    if user_id is None:
        abort(404)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def POST_request_user():
    """"post request"""
    data = request.get_json()
    if not data:
        return abort(400, {'message': 'Not a JSON'})
    if 'email' not in data:
        abort(400)
        return abort(400, {'message': 'Missing email'})
    if 'password' not in data:
        abort(400)
        return abort(400, {'message': 'Missing password'})
    # creation of a new user
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def PUT_user(user_id):
    """Put request"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if not data:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in data.items():
        if key not in ["id", "created_at", "email", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
