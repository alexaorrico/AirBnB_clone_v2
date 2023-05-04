#!/usr/bin/python3
"""
handles REST API actions for State
"""
from api.v1.views import app_views
from flask import jsonify
from flask import Flask
from flask import request
from flask import abort
from models import storage
from models.user import User


@app_views.route(
    '/users',
    methods=['GET', 'POST'],
    strict_slashes=False)
def users():
    """handles states route"""
    my_users = storage.all("User")

    if request.method == 'GET':
        return jsonify(
            [obj.to_dict() for obj in my_users.values()])
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data is None or type(post_data) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        email = post_data.get('email')
        if email is None:
            return jsonify({'error': 'Missing email'}), 400
        password = post_data.get('password')
        if password is None:
            return jsonify({'error': 'Missing password'}), 400
        new_user = User(**post_data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route(
    '/users/<string:user_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False)
def user_with_id(user_id):
    """handles states route with a parameter state_id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        put_data = request.get_json()
        if put_data is None or type(put_data) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        to_ignore = ['id', 'created_at', 'updated_at', 'email']
        user.update(to_ignore, **put_data)
        return jsonify(user.to_dict()), 200
