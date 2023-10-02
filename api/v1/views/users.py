#!/usr/bin/python3
"""module to handle requests regarding a User object"""

from models.user import User
from models import storage
from api.v1.views import app_views
import json
from flask import request, jsonify, abort


@app_views.route("/users", strict_slashes=False)
def get_users():
    """retrieves a list of all User objects"""
    users = storage.all(User)
    users_list = [user.to_dict() for user in users.values()]

    if len(users_list) == 0:
        abort(404)
    return jsonify(users_list)


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user_by_id(user_id):
    """retrieves a user by their id"""
    response = storage.get(User, user_id)

    if response is None:
        abort(404)

    return jsonify(response.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user_obj(user_id):
    """deletes a State object"""
    # print("trying")
    user_to_delete = storage.get(User, user_id)
    # print("delete this ", user_to_delete)

    if user_to_delete is None:
        abort(404)

    storage.delete(user_to_delete)
    storage.save()
    # print("saving")
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_new_user():
    """creates a User object"""
    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400, description="Content-Type is not application/json")

    # if password not in dict
    if data_entered.get('password') is None:
        abort(400, description="Missing password")
    if data_entered.get('email') is None:
        abort(400, description="Missing email")

    new_user = User(**data_entered)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_obj(user_id):
    """updates a User object"""
    user_to_update = storage.get(User, user_id)

    if user_to_update is None:
        abort(404)

    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400, description="Content-Type is not application/json")

    for key, value in data_entered.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_to_update, key, value)

    storage.save()

    return jsonify(user_to_update.to_dict()), 200
