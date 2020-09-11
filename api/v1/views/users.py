#!/usr/bin/python3
""" flask module to manage the stored users """
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route(
    '/users',
    strict_slashes=False,
    methods=['GET', 'POST']
)
@app_views.route(
    '/users/<string:user_id>',
    strict_slashes=False, methods=['GET', 'PUT', 'DELETE']
)
def users(user_id=None):
    """ handles all default RestFul API actions inside users"""
    if request.method == 'GET' and user_id is None:
        return all_users()
    elif request.method == 'GET' and user_id:
        return get_user(user_id)
    elif request.method == 'DELETE':
        return delete_user(user_id)
    elif request.method == 'POST':
        return create_user()
    elif request.method == 'PUT':
        return update_user(user_id)


def update_user(user_id):
    """ it update an user """
    ignored_keys = ['id', 'created_at', 'updated_at', 'email']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_json = request.get_json()
    if user_json is None:
        abort(400, 'Not a JSON')

    for key in user_json.keys():
        if key not in ignored_keys:
            setattr(user, key, user_json[key])
    storage.save()
    return jsonify(user.to_dict()), 200


def create_user():
    """ it create an user from a http request
    the new user information is expected to be
    json string
    """
    user_json = request.get_json()
    if user_json is None:
        abort(400, 'Not a JSON')
    if user_json.get('name') is None:
        abort(400, "Missing name")
    if user_json.get('email') is None:
        abort(400, "Missing email")
    if user_json.get('password') is None:
        abort(400, "Missing password")
    user = User(**user_json)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


def delete_user(user_id):
    """ it delete the user corresponding to the user_id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


def get_user(user_id):
    """ it get the user corresponding to the user_id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


def all_users():
    """ it retrieve all the users """
    users_list = []
    for user in storage.all(User).values():
        users_list.append(user.to_dict())
    return jsonify(users_list)
