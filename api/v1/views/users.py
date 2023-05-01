#!/usr/bin/python3

""" Handles all restful API actions for State"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from models import storage


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Returns all users """

    user_objs = storage.all(User)
    users = [obj.to_dict() for obj in user_objs.values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_individual_users(user_id):
    """" Returns indivuidual users by id """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes individual users by id """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    """ Delete the user """
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def create_users():
    """ Creates a new user by using the URL """

    my_dict = request.get_json()

    if my_dict is None:
        abort(400, 'Not a JSON')
    if my_dict.get("email") is None:
        abort(400, 'Missing email')
    if my_dict.get("password") is None:
        abort(400, 'Missing password')

    new_user = User(**my_dict)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates an user by user ID """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    my_dict = request.get_json()

    if my_dict is None:
        abort(400, 'Not a JSON')

    for k, v in my_dict.items():
        setattr(user, k, v)

    user.save()
    return jsonify(user.to_dict()), 200
