#!/usr/bin/python3
"""
a new view for User object that handles
all default RESTFul API actions
"""


from api.v1.views import app_views
from models import storage
from models.user import User
from flask import Flask, make_response, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """
    Retrieves the list of all User objects

    Returns:
        json: Wanted User object with status code 200.
    """
    users = storage.all(User)
    list = []

    for user in users.items():
        list.append(user.to__dict())
    return make_response(jsonify(list), 200)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def single_user(user_id):
    """
    Retrieves a specified User object.

    Args:
        user_id : ID of the specified User object.

    Raises:
        NotFound: Raises a 404 error if user_id
        is not linked to any User object.

    Returns:
        json: Wanted User object with status code 200.
    """
    user = storage.get(User, user_id)

    if user is None:
        raise NotFound

    return make_response(jsonify(user.to__dict()), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
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


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """
    Creates a new User object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'name' is not
        present sends status code 400.

    Returns:
        json: The new User with the status code 201.
    """
    user = User(**request.get_json())

    if not request.get_json:
        return make_response('Not a JSON', 400)

    if 'email' not in request.get_json.keys():
        return make_response('Missing email', 404)

    if 'password' not in request.get_json.keys():
        return make_response('Missing password', 404)

    user.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Update a specified User object.

    Args:
        user_id : Id of the wanted User object.

    Returns:
        json: The updated User object with the status code 200.
    """
    user = storage.get(User, user_id)

    if not request.get_json:
        return make_response('Not a JSON', 400)

    if user is None:
        raise NotFound

    for key, usr in request.get_json().items():
        if key not in ('id', 'created_at', 'updated_at'):
            user.__setattr__(key, usr)

    user.save()

    return make_response(jsonify(user.to__dict()), 200)
