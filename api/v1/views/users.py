#!/usr/bin/python3
"""
    Handles default RestFul API actions for User objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route(
    '/users',
    methods=['GET', 'POST'],
    strict_slashes=False
)
def users_all():
    """
        Handle all objects
    """
    list_of_users = []
    objects = storage.all(User).values()
    for obj in objects:
        list_of_users.append(obj.to_dict())

    if request.method == 'GET':
        return jsonify(list_of_users)

    if request.method == 'POST':
        try:
            request_dict = request.get_json()
        except:
            abort(400, 'Not a JSON')

        if 'email' not in request_dict.keys():
            abort(400, 'Missing email')

        if 'password' not in request_dict.keys():
            abort(400, 'Missing password')

        new_User = User(**request_dict)
        new_User.save()

        return jsonify(new_User.to_dict()), 201


@app_views.route(
    '/users/<user_id>',
    methods=['GET', 'PUT', 'DELETE'],
    strict_slashes=False
)
def users_by_id(user_id):
    """
        Handle objects by ID
    """

    User_obj = storage.get(User, user_id)
    if User_obj is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(User_obj.to_dict())

    if request.method == 'DELETE':
        User_obj.delete()
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        try:
            request_dict = request.get_json()
        except:
            abort(400, 'Not a JSON')

        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, value in request_dict.items():
            if key in ignore_keys:
                continue
            setattr(User_obj, key, value)
        User_obj.save()

        return jsonify(User_obj.to_dict()), 200
