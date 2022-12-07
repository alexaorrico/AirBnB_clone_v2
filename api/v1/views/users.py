#!/usr/bin/python3
"""Views for the User class: GET, DELETE,  POST, PUT"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    objs = []
    for x in storage.all(User).values():
        objs.append(x.to_dict())
    return jsonify(objs)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    obj = User(**request.get_json())
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    user.__dict__.update(request.get_json())
    old_dict = user.to_dict()
    storage.delete(user)
    user = User(**old_dict)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 200
