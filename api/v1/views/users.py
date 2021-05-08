#!/usr/bin/python3
"""Amenity views"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def users_get():
    """Retrieves the list of all User objects"""
    all_users = storage.all('User').values()
    users_for_json = []
    for user in all_users:
        users_for_json.append(user.to_dict())
    return jsonify(users_for_json)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_users(user_id):
    """Retrieves the list of all User objects"""
    if storage.get('User', user_id) is None:
        abort(404)
    return jsonify(storage.get('User', user_id).to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes an User object"""
    if not storage.get('User', user_id):
        abort(404)
    else:
        storage.get('User', user_id).delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    """Creates an User"""
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if "email" not in req:
        abort(400, "Missing email")
    if "password" not in req:
        abort(400, "Missing password")
    new_user = User(email=request.json["email"],
                    password=request.json['password'])
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_users(user_id):
    """Updates an User object"""
    req = request.get_json()
    if not request.json:
        abort(400, "Not a JSON")
    user_to_modify = storage.get('User', user_id)
    if user_to_modify is None:
        abort(404)
    for key in req:
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_to_modify, key, req[key])
    storage.save()
    return jsonify(user_to_modify.to_dict()), 200
