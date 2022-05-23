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
        UserList = []
        User_all = storage.all(User)

        for key, value in User_all.items():
            UserList.append(value.to_dict())
        return jsonify(UserList)

    elif request.method == 'POST':
        body_request_dict = request.get_json()

        if not body_request_dict:
            abort(400, 'Not a JSON')

        if 'email' not in body_request_dict:
            abort(400, 'Missing email')

        if 'password' not in body_request_dict:
            abort(400, 'Missing password')

        newUser = User(**body_request_dict)
        storage.new(newUser)
        storage.save()

        return newUser.to_dict(), 201


@app_views.route('/User/<User_id>', methods=['GET', 'DELETE', 'PUT'])
def User_User_id(User_id):
    """
        Retrieves a User object
    """
    User_catch = storage.get(User, User_id)

    if User_catch is None:
        abort(404)

    if request.method == 'GET':
        return User_catch.to_dict()

    if request.method == 'DELETE':
        storage.delete(User_catch)
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        body_request_dict = request.get_json()

        if not body_request_dict:
            return 'Not a JSON', 400

        for key, value in body_request_dict.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(User_catch, key, value)

        User_catch.save()
        return User_catch.to_dict(), 200
