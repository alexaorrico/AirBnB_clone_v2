#!/usr/bin/python3
"""states module"""
from api.v1.views import app_views
from flask import jsonify, Flask, abort, request, make_response
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def all_users():
    """return json"""
    for user in storage.all(User).values():
        all_user = [user.to_dict()]
    return jsonify(all_user)


@app_views.route("/users/<string:user_id>", methods=['GET'],
                 strict_slashes=False)
def all_user_by_id(user_id):
    """return json"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_users_by_id(user_id):
    """return json"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def post_user():
    """return json"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = request.get_json()
    us = User(**user)
    us.save()
    return make_response(jsonify(us.to_dict()), 201)


@app_views.route("/users/<string:user_id>", methods=['PUT'],
                 strict_slashes=False)
def put_user_by_id(user_id):
    """return json"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
