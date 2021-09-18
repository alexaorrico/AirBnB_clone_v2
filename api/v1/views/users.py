#!/usr/bin/python3
"""
    API view related to User objects that handles all the default
    actions.
"""
import requests
from api.v1.views import app_views
from models import storage
from models.user import User
import json
from werkzeug.exceptions import BadRequest, NotFound
from flask import Flask, request, jsonify, make_response


def __is_valid_json(data):
    """
    Checks if the given data is a valid json.

    Args:
        data : Data to check

    Returns:
        True: If data is a valid json.
        False: If data is not a valid json.
    """
    try:
        json.loads(data)

        return True
    except Exception:
        return False


@app_views.route('/users', methods=['GET'])
def users_list() -> json:
    """
    Retrieves the list of all User objects.

    Returns:
        json: List of User objects with status code 200.
    """
    users = storage.all(User)
    list = []
    for key, user in users.items():
        list.append(user.to_dict())
    return make_response(jsonify(list), 200)


@app_views.route('/users/<user_id>', methods=['GET'])
def user_show(user_id) -> json:
    """
    Retrieves a specified User object.

    Args:
        user_id : ID of the wanted User object.

    Raises:
        NotFound: Raises a 404 error if user_id
        is not linked to any User object.

    Returns:
        json: Wanted User object with status code 200.
    """
    user = storage.get(User, user_id)

    if user is None:
        raise NotFound

    return make_response(jsonify(user.to_dict()), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def user_delete(user_id) -> json:
    """
    Deletes a specified User object.

    Args:
        user_id : ID of the wanted User object.

    Raises:
        NotFound: Raises a 404 error if user_id
        is not linked to any User object.

    Returns:
        json: Empty dictionary with the status code 200.
    """
    user = storage.get(User, user_id)

    if user is None:
        raise NotFound

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users/', methods=['POST'])
def user_create() -> json:
    """
    Creates a new User object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'email' or 'password'
        is not present sends status code 400.

    Returns:
        json: The new User with the status code 201.
    """
    data = request.get_data()

    if not __is_valid_json(data):
        return make_response('Not a JSON', 400)

    data = json.loads(data)

    if 'email' not in data.keys():
        return make_response('Missing email', 400)

    if 'password' not in data.keys():
        return make_response('Missing password', 400)

    user = User(data)
    for key, value in data.items():
        user.__setattr__(key, value)
    storage.new(user)
    storage.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def user_update(user_id) -> json:
    """
    Update a specified State object.

    Args:
        state_id : Id of the wanted State object.

    Returns:
        json: The updated State object with the status code 200.
    """

    data = request.get_data()

    if not __is_valid_json(data):
        return make_response('Not a JSON', 400)

    data = json.loads(data)
    user = storage.get(User, user_id)

    if user is None:
        raise NotFound

    for key, value in data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            user.__setattr__(key, value)

    storage.new(user)
    storage.save()

    return make_response(jsonify(user.to_dict()), 200)
