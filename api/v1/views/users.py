#!/usr/bin/python3
"""View for Users"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.user import User
from flask import abort
from flask import make_response
from flask import request


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def all_users():
    """Return all users"""
    dict_users = storage.all(User)
    list_users = []
    for v in dict_users.values():
        list_users.append(v.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_users(user_id):
    """Return user according class and id of user
        or return Error: Not found if it doesn't exist.
    """
    if user_id:
        dict_users = storage.get(User, user_id)
        if dict_users is None:
            abort(404)
        else:
            return jsonify(dict_users.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """Deletes an object User if exists, otherwise raise
        404 error
    """
    if user_id:
        users = storage.get(User, user_id)
        if users is None:
            abort(404)
        else:
            storage.delete(users)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def response_user():
    """Post request that allow to create a new user if exists the name
        or raise error if is not a valid json or if the name is missing
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    if "email" not in req:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in req:
        return make_response(jsonify({"error": "Missing password"}), 400)
    users = User(**req)
    users.save()
    return make_response(jsonify(users.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """Updates attributes from an user object"""
    if user_id:
        users = storage.get(User, user_id)
        if users is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(users, key, value)
        users.save()
        return make_response(jsonify(users.to_dict()), 200)
