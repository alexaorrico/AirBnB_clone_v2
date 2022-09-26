#!/usr/bin/python3
"""
    view for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def User():
    """
        Retrieves the list of all User objects and create a new User"
    """

    if request.method == 'GET':
        UserList = []
        User = storage.all(User)

        for User in User.values():
            UserList.append(User.to_dict())

        return jsonify(UserList)

    elif request.method == 'POST':
        body_request_dict = request.get_json()

        if not body_request_dict:
            abort(400, 'Not a JSON')

        if "name" not in body_request_dict:
            abort(400, 'Missing name')

        newUser = User(**body_request_dict)
        storage.new(newUser)
        storage.save()

        return newUser.to_dict(), 201


@app_views.route('/User/<User_id>', methods=['GET', 'DELETE', 'PUT'])
def User_User_id(User_id):
    """
        Retrieves a User object
    """
    User = storage.get(User, User_id)

    if User is None:
        abort(404)

    if request.method == 'GET':
        return User.to_dict()

    if request.method == 'DELETE':
        storage.delete(User)
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        body_request_dict = request.get_json()

        if not body_request_dict:
            return 'Not a JSON', 400

        for key, value in body_request_dict.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(User, key, value)

        User.save()
        return User.to_dict(), 200
