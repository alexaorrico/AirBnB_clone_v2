#!/usr/bin/python3
""" creates a new view for user object """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def get_users():
    """ get list of users """
    users = storage.all(User).values()
    if not users:
        abort(404)

    all_users = []
    for user in users:
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ get user by id """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ deletes a user """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def post_user():
    """ post method for adding a user """
    res = request.get_json()
    if not res:
        abort(400, description="Not a JSON")

    if 'email' not in res:
        abort(400, description="Missing email")

    if 'password' not in res:
        abort(400, description="Missing password")

    user = User(**res)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ updates user based on id """
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
