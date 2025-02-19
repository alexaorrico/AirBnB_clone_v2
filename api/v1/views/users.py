#!/usr/bin/python3
"""RESTful API for class User"""

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_users.yml', methods=['GET'])
def get_users():
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def post_user():
    res = request.get_json()
    if not res:
        return abort(400, description="Not a JSON")
    if 'email' not in res:
        return abort(400, description="Missing email")
    if 'password' not in res:
        return abort(400, description="Missing password")
    new_user = User(**res)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def put_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    res = request.get_json()
    if not res:
        return abort(400, description="Not a JSON")
    for key, value in res.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200

