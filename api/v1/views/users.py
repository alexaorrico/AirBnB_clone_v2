#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, jsonify, request
import json


@app_views.route('/users', methods=['GET'])
def all_users():
    users_dict = storage.all(User)
    users_list = [user.to_dict() for user in users_dict.values()]
    return users_list


@app_views.route('/users/<user_id>', methods=['GET'])
def users_id(user_id):
    user = storage.get(User, user_id)
    if user:
        return user.to_dict(), 201
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def users_delete(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify('{}'), 201


@app_views.route('/users', methods=['POST'])
def users_post():
    try:
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        if 'email' not in data_object:
            abort(400, 'Missing email')
        if 'password' not in data_object:
            abort(400, 'Missing password')
        new_user = User(**data_object)
        storage.new(new_user)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def users_put(user_id):
    try:
        user_up = storage.get(User, user_id)
        if not user_up:
            abort(404)
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        for key, value in data_object.items():
            setattr(user_up, key, value)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(user_up.to_dict()), 201
