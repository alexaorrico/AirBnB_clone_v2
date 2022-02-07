#!/usr/bin/python3
""" Module for User objects that handles all default RESTFul API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieves list of all User objects """
    all_users = storage.all(User).values()
    users_list = []

    for user in all_users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ Creates a User """
    request_data = request.get_json()

    if not request_data:
        abort(400, description="Not a JSON")

    if 'email' not in request_data:
        abort(400, description="Missing email")
    if 'password' not in request_data:
        abort(400, description="Missing password")

    new_user = User()
    new_user.email = request_data['email']
    new_user.password = request_data['password']

    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    for key, value in request_data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
