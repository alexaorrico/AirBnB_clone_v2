#!/usr/bin/python3
"""
    API module User
"""

import models
from models import storage
from models.user import *

from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """
        A function that Retrieves the list
        of all User objects: GET /api/v1/users
    """
    # get all saved state objects
    objs = storage.all(User).values()

    # Convert state object to dictionary and save in list
    amenityList = [obj.to_dict() for obj in objs]

    return jsonify(amenityList)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """
        A function that Retrieves a User
        object: GET /api/v1/users/<user_id>
    """
    obj = storage.get(User, user_id)

    if (obj):
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """
        A function that Deletes a User object:
        DELETE /api/v1/users/<user_id>
    """
    obj = storage.get(User, user_id)

    # delete and save if state object is found, if not return error 404
    if (obj):
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def add_user():
    """
        A function that Creates a User: POST /api/v1/users
    """
    # Check If the HTTP body request is not valid JSON
    if (not request.get_json()):
        abort(400, 'Not a JSON')

    json_str = request.get_json()

    if ('email' not in json_str):
        abort(400, 'Missing email')
    if ('password' not in json_str):
        abort(400, 'Missing password')

    # create a new state object, save and return it
    obj = User(**json_str)
    obj.save()

    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
        A function that Updates a User object:
        PUT /api/v1/users/<user_id>
    """
    obj = storage.get(User, user_id)
    if (obj):

        json_str = request.get_json()
        # Check If the HTTP body request is not valid JSON
        if (not json_str):
            abort('400', 'Not a JSON')

        # Update state object attributes
        to_ignore = ['id', 'email', 'created_at', 'updated_at']
        for key, value in json_str.items():
            if key not in to_ignore:
                setattr(obj, key, value)

        #  save and return
        obj.save()
        return jsonify(obj.to_dict()), 200
    else:
        abort(404)
