#!/usr/bin/python3
"""
users
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_full_users_method():
    new_dict = []
    for obj in storage.all(User).values():
        new_dict.append(obj.to_dict())
    return jsonify(new_dict)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_method(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_method(user_id):
    if user_id is None:
        abort(404)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user_method():
    res = request.get_json()
    if not isinstance(res, dict):
        abort(400, {'message': 'Not a JSON'})
    if 'email' not in res:
        abort(400, {'message': 'Missing email'})
    if 'password' not in res:
        abort(400, {'message': 'Missing password'})
    new_user = User(**res)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user_method(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    res = request.get_json()
    if not isinstance(res, dict):
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
