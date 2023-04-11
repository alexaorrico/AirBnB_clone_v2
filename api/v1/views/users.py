#!/usr/bin/python3
""" handles all default RESTFul API actions for User """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_user():
    """ retrieves the list of all users """
    users = storage.all(User)
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    """ retrieves a User by its id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        user_id = user.to_dict()
    return jsonify(user_id)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ deletes a User by its id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ creates a User """
    data_json = request.get_json()
    if data_json is None:
        abort(400, description="Not a JSON")
    elif 'email' not in data_json:
        abort(400, description="Missing email")
    elif 'password' not in data_json:
        abort(400, description="Missing password")
    else:
        new_user = User(**data_json)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ updates a User by its id """
    user = storage.get(User, user_id)
    data_json = request.get_json()
    if user is None:
        abort(404)
    elif data_json is None:
        abort(400, description="Not a JSON")
    else:
        for key, value in data_json.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
