#!/usr/bin/python3
"""users file"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from models import storage


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def alluser():
    """list of all user objects"""

    list = []
    users = storage.all(User)
    for user in users.values():
        list.append(user.to_dict())
    return jsonify(list)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    """list one user object"""
    
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return user.to_dict()


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def user_delete(user_id):
    """Delete a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        user.delete()
        storage.save()
        return {}, 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def user_post():
    """list of all user objects"""

    body = request.get_json()
    if body is None:
        abort(400, description="Not a JSON")
    if 'email' not in body.keys():
        abort(400, description="Missing email")
    if 'password' not in body.keys():
        abort(400, description="Missing password")
    user = User(**body)
    user.save()
    return user.to_dict(), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    """list of all user objects"""

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, description="Not a JSON")
    ignored_keys = ('id', 'email', 'created_at', 'updated_at')
    for key, value in body.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    storage.save()
    return user.to_dict(), 200
