#!/usr/bin/python3
"""Creating user api app"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET', 'POST'], strict_slashes=False)
def allUsers():
    """retrieves a list of all users in db"""
    if request.method == "GET":
        all_users = []
        for key in storage.all(User).values():
            all_users.append(key.to_dict())
        return jsonify(all_users)

    if request.method == "POST":
        if not request.is_json:
            return "Not a JSON", 400

        jsonReq = request.get_json()

        if 'email' not in jsonReq:
            return "Missing email\n", 400
        if 'password' not in jsonReq:
            return "Missing password\n", 400

        newUser = User(**jsonReq)

        storage.new(newUser)
        storage.save()

        return jsonify(newUser.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def user_id(user_id):
    """updates user_id"""
    if request.method == 'GET':
        user_data = storage.get(User, user_id)
        if user_data is not None:
            return jsonify(user_data.to_dict())
        abort(404)

    if request.method == "PUT":
        user_data = storage.get(User, user_id)
        if user_data is not None:
            ignoreKeys = ['id', 'email', 'created_at', 'updated_at']

            if not request.is_json:
                return "Not a JSON", 400
            for key, value in request.get_json().items():
                if key not in ignoreKeys:
                    setattr(user_data, key, value)
            storage.save()
            return jsonify(user_data.to_dict()), 200
        abort(404)

    if request.method == "DELETE":
        user_data = storage.get(User, user_id)
        if user_data:
            storage.delete(user_data)
            storage.save()
            return jsonify({}), 200
        abort(404)
