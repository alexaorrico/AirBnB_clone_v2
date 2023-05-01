#!/usr/bin/python3
"""
view for User object that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from models.user import User
from flask import jsonify, abort, make_response, request
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False,)
def get_users():
    """ return all user objects """
    users = storage.all(User)
    all_users = [user.to_dict() for user in users.values()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user_byid(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def insert_user():
    """ Creates a User: POST /api/v1/users """
    request = request.get_json()
    if not request:
        abort(400, description="Not a JSON")
    if "email" not in request:
        abort(400, description="Missing email")
    if "password" not in request:
        abort(400, description="Missing password")
    new_user = User(**request)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object: PUT /api/v1/users/<user_id> """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']

    for key, value in req.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
