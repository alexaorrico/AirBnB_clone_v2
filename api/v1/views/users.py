#!/usr/bin/python3
"""
    This module creates a new view for State
    objects that handles all default REST API
    actions.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves all users in storage"""
    all_users = storage.all(User).values()
    user_list = []
    for user in all_users:
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def get_specific_user(user_id):
    """Return the user with given id"""
    search_result = storage.get(User, user_id)
    if search_result:
        return jsonify(search_result.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_specific_user(user_id):
    """Delete the user with given id"""
    search_result = storage.get(User, user_id)
    if search_result:
        storage.delete(search_result)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/users/", methods=['POST'],
                 strict_slashes=False)
def post_new_user():
    """Post a new user to the db"""
    try:
        usr_dict = request.get_json()

    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    if usr_dict.get("email"):
        if usr_dict.get("password"):
            new_usr = User(**usr_dict)
            storage.new(new_usr)
            storage.save()
            return jsonify(new_usr.to_dict()), 201
        else:
            return jsonify({"error": "Missing password"}), 400
    else:
        return jsonify({"error": "Missing name"}), 400


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def modify_user(user_id):
    """Modify an existing user in the db"""
    user = storage.get(User, user_id)
    if user:
        try:
            update_dict = request.get_json()
            for key in ('id', 'created_at', 'updated_at'):
                if update_dict.get(key):
                    del update_dict[key]

        except Exception:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in update_dict.items():
            setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200

    else:
        abort(404)
