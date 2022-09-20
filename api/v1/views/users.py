#!/usr/bin/python3

""" Module handling requests for User objects """

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/users', strict_slashes=False,
                 methods=['GET', 'POST'])
def all_users():
    """ Handles GET and POST request for all users """
    if request.method == 'GET':
        user_objects = storage.all(User)
        user_list = []
        for key, val in user_objects.items():
            user_list.append(val.to_dict())
        return jsonify(user_list)

    if request.method == 'POST':
        data = request.get_json(silent=True)
        user = User()
        if data is None:
            return 'Not a JSON', 400
        if 'email' not in data.keys():
            return 'Missing email', 400
        if 'password' not in data.keys():
            return 'Missing password', 400
        ignored_keys = ['id', 'created_at', 'updated_at']
        for key in data:
            if key not in ignored_keys:
                setattr(user, key, data[key])
        user.save()
        return(user.to_dict()), 201
    abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user_by_id(user_id):
    """ Handles GET, DELETE and PUT requests for amenity by id """
    if request.method == 'GET':
        user_objects = storage.all(User)
        for key, val in user_objects.items():
            if val.id == user_id:
                return val.to_dict()
        abort(404)

    if request.method == 'DELETE':
        user_objects = storage.all(User)
        for key, val in user_objects.items():
            if val.id == user_id:
                storage.delete(val)
                storage.save()
                return {}, 200
        abort(404)

    if request.method == 'PUT':
        try:
            valid_request = request.get_json()
        except Exception:
            return 'Not a JSON', 400

        ignored_keys = ['id', 'created_at', 'updated_at']
        user_objects = storage.all(User)
        for key, val in user_objects.items():
            if val.id == user_id:
                for key in valid_request:
                    if key not in ignored_keys:
                        setattr(val, key, valid_request[key])
                storage.save()
                return val.to_dict(), 200
        abort(404)
