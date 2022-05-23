#!/usr/bin/python3
"""
    view for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """
        Retrieves the list of all User objects and create a new User"
    """

    if request.method == 'GET':
        user_all = storage.all(User)
        users_json = []
        for key, value in user_all.items():
            users_json.append(value.to_dict())
        return jsonify(users_json)

    elif request.method == 'POST':
        body_request_dict = request.get_json()

        if not body_request_dict:
            abort(400, 'Not a JSON')

        if 'email' not in body_request_dict:
            abort(400, 'Missing email')

        if 'password' not in body_request_dict:
            abort(400, 'Missing password')

        new_state = User(**body_request_dict)
        storage.new(new_state)
        storage.save()
        return new_state.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_id(user_id):
    """
        Retrieves a User object
    """
    user_catch = storage.get(User, user_id)

    if user_catch is None:
        abort(404)

    if request.method == 'GET':
        return user_catch.to_dict()

    if request.method == 'DELETE':
        storage.delete(user_catch)
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        body_request_dict = request.get_json()

        if not body_request_dict:
            abort(400, 'Not a JSON')

        for key, value in body_request_dict.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user_catch, key, value)

        user_catch.save()
        return user_catch.to_dict(), 200
