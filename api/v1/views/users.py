#!/usr/bin/python3
""" a new view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET', 'POST'], strict_slashes=False)
def _users():
    """retrieves the list of all user objects
    """
    if request.method == "GET":
        all_users = []
        for key in storage.all("User").values():
            all_users.append(key.to_dict())
        return jsonify(all_users)

    if request.method == 'POST':
        if not request.is_json:
            return "Not a JSON", 400

        all_users = User(**request.get_json())
        if "password" not in all_users.to_dict().keys():
            return "Missing password", 400

        if "email" not in all_users.to_dict().keys():
            return "Missing email", 400

        all_users.save()
        return all_users.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def user_id(user_id):
    """updates a user object
    """
    if request.method == "GET":
        user_info = storage.get(User, user_id)
        if user_info is not None:
            return user_info.to_dict()
        abort(404)

    if request.method == "PUT":
        user_info = storage.get(User, user_id)
        if user_info is not None:
            if not request.is_json:
                return "Not a JSON", 400

            for key, value in request.get_json().items():
                setattr(user_info, key, value)
            storage.save()
            return user_info.to_dict(), 200
        abort(404)

    if request.method == "DELETE":
        user_info = storage.get(User, user_id)
        if user_info is not None:
            user_info.delete()
            storage.save()
            return {}, 200
        abort(404)
