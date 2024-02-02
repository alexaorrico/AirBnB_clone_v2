#!/usr/bin/python3
'''View to handle the RESTful API actions for 'User' objects'''
from flask import jsonify, request, abort

from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    '''Handles "/users" route'''
    if request.method == 'GET':
        users = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(users)

    if request.method == 'POST':
        data = request.get_json()
        if data is None or type(data) is not dict:
            return 'Not a JSON', 400
        email = data.get('email')
        password = data.get('password')
        if email is None:
            return 'Missing email', 400
        if password is None:
            return 'Missing password', 400
        user = User(**data)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def user_actions(user_id):
    '''Handles actions for "/users/<user_id>" route'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None or type(data) is not dict:
            return 'Not a JSON', 400
        for attr, val in data.items():
            if attr not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, attr, val)
        user.save()
        return jsonify(user.to_dict()), 200
