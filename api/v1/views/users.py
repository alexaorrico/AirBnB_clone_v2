#!/usr/bin/python3
""" View User """

import models
from flask import jsonify, abort
from flask import request as req
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET', 'POST'])
def user_objects():
    """Retrieves all amenities with a list of objects"""
    if req.method == 'GET':
        users = models.storage.all('User')
        users = [u.to_dict() for u in users.values()]
        return jsonify(users)

    if req.method == 'POST':
        reqj = req.get_json()
        if reqj is None:
            abort(400, 'Not a JSON')
        if reqj.get('email', None) is None:
            abort(400, 'Missing email')
        if reqj.get('password', None) is None:
            abort(400, 'Missing password')
        user = User(**reqj)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_res(user_id):
    """id Amenity retrieve json object"""
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
