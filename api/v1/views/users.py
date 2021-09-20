#!/usr/bin/python3
""" View User """

import models
from flask import jsonify, abort
from flask import request as req
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET', 'POST'])
def usersAll():
    """Returns user objects as JSON response"""
    if req.method == 'GET':
        users = models.storage.all('User')
        users = [u.to_dict() for u in users.values()]
        return jsonify(users)

    if req.method == 'POST':
        body = req.get_json()
        if body is None:
            abort(400, 'Not a JSON')
        if body.get('email', None) is None:
            abort(400, 'Missing email')
        if body.get('password', None) is None:
            abort(400, 'Missing password')
        user = User(**body)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def usersId(user_id):
    """Returns a User object as JSON response"""
    user = models.storage.get('User', user_id)
    if user is None:
        abort(404)

    if req.method == 'GET':
        return jsonify(user.to_dict())

    if req.method == 'PUT':
        user_json = req.get_json()
        if user_json is None:
            abort(400, 'Not a JSON')
        ignore = ['id', 'email', 'created_at', 'updated_at']
        for key, val in user_json.items():
            if key not in ignore:
                user.__setattr__(key, val)
        models.storage.save()
        return jsonify(user.to_dict())

    if req.method == 'DELETE':
        user.delete()
        models.storage.save()
        return jsonify({})
