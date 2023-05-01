#!/usr/bin/python3
"""
Handle all default RESTFUL API actions
"""
from models.user import User
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify
from models import storage


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def users():
    """ Returns all users"""
    users = storage.all('User')
    if users is None:
        abort(404)

    if request.method == 'GET':
        all_users = []
        for user in users.values():
            all_users.append(user.to_dict())
        return jsonify(all_users)
    if request.method == 'POST':
        data = request.get_json()
        if not request.is_json:
            abort(400, 'Not a JSON')
        if 'email' not in data:
            abort(400, 'Missing email')
        if 'password' not in data:
            abort(400, 'Missing password')
        new_user = User(**data)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def user(user_id):
    """ Returns city object of id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        if user:
            return jsonify(user.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        if not request.is_json:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            ign_attr = ['id', 'created_at', 'updated_at']
            if k not in ign_attr:
                setattr(user, k, v)
        storage.save()
        return jsonify(user.to_dict()), 200

    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
