#!/usr/bin/python3
"""Users """

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def all_users():
    """get users"""
    users = []
    for user in storage.all('User').values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<string:user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get specified user"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return (jsonify({}))


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def createuser():
    """create a user"""
    djson = request.get_json()
    if not djson:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in djson:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in djson:
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**djson)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'], strict_slashes=False)
def updateuser(user_id):
    """update user based on ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    json = request.get_json()
    if not djson:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in djson.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return (jsonify(user.to_dict()), 200)
