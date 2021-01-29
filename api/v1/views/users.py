#!/usr/bin/python3
""" a new view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.user import User


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>/', methods=['GET'], strict_slashes=False)
def users_get(user_id):
    """retrieves the list of all User objects
    """
    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return jsonify(users)

    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_users(user_id):
    """deletes a User object
    """
    user = storage.get('User', user_id)
    if user is None:
        return jsonify(abort(404))
    user.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_users():
    """creates a user
    """
    info = request.get_json()
    if info is None:
        return (jsonify({"Not a JSON"}), 400)

    name = info.get('name')
    if name is None:
        return (jsonify({"Missing email"}), 400)

    password = info.get("password")
    if password is None:
        return (jsonify({"Missing password"}), 400)

    user_post = User(**info)
    user_post.save()

    return (jsonify(user_post.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_users(user_id):
    """updates a state object
    """
    info = request.get_json()
    if info is None:
        return jsonify(abort(400, 'Not a JSON'))

    user_info = storage.get("User", user_id)
    if user_info is None:
        abort(404)

    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in info.items():
        if key not in ignore_keys:
            setattr(user_info, key, value)

    state_info.save()
    return jsonify(user_info.to_dict())
