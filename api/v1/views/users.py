#!/usr/bin/python3
"""Modules that handles all Restful API actions for User"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users_list():
    """Returns collection of all users"""
    users = []
    all_users = storage.all(User).values()
    for usr in all_users:
        users.append(usr.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    """Returns an object user"""
    usr = storage.get(User, user_id)
    if usr is None:
        abort(404)
    return jsonify(usr.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a given user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Creates a new given user"""
    new_user = request.get_json()
    if not new_user:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'email' not in new_user:
        return jsonify({'error': 'Missing email'}), 400
    elif 'password' not in new_user:
        return jsonify({'error': 'Missing password'}), 400
    else:
        new_obj = User(**new_user)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """updates a given user"""
    user_to_update = request.get_json()
    if not user_to_update:
        return jsonify({'error': 'Not a JSON'}), 400

    my_dict = storage.get(User, user_id)
    if my_dict:
        for key, value in user_to_update.items():
            setattr(my_dict, key, value)
        storage.save()
        return jsonify(my_dict.to_dict()), 200
    else:
        abort(404)
