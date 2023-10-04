#!/usr/bin/python3
""" Users """
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request, make_response
from sqlalchemy.exc import IntegrityError


@app_views.route('/users',
                 methods=['GET'],
                 strict_slashes=False
                 )
def list_users():
    """List all `User` objects"""
    users_dict = storage.all(User)
    users_list = []
    for user in users_dict.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'],
                 strict_slashes=False
                 )
def get_user(user_id):
    """Retrieves a `User` object."""
    user = storage.get(User, user_id)
    if user is not None:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False
                 )
def delete_user(user_id):
    """Deletes a `User` object."""
    user = storage.get(User, user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/users',
                 methods=['POST'],
                 strict_slashes=False
                 )
def create_user():
    """Creates a `User` object."""
    request_dict = request.get_json(silent=True)
    if request_dict is not None:
        if 'email' not in request_dict.keys() or request_dict['email'] is None:
            return make_response(jsonify({'error': 'Missing email'}), 400)
        if 'password' not in request_dict.keys()\
           or request_dict['password'] is None:
            return make_response(jsonify({'error': 'Missing password'}), 400)
        new_user = User(**request_dict)
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)
    return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False
                 )
def update_user(user_id):
    """Updates a `User` object."""
    request_dict = request.get_json(silent=True)
    if request_dict is not None:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        for key, val in request_dict.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, val)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)
