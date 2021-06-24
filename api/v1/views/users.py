#!/usr/bin/python3

""" Module to handle amenities RESTful API """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def all_users():
    users = storage.all(User).values()

    if request.method == 'GET':
        return jsonify(list(map(lambda x: x.to_dict(), users)))

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'email' not in request.json:
            abort(400, 'Missing email')
        if 'password' not in request.json:
            abort(400, 'Missing password')
        obj = User(**request.get_json())
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['DELETE', 'GET', 'PUT'],
                 strict_slashes=False)
def one_user(user_id):
    users = storage.all(User).values()
    user = [user for user in users if user.id == user_id]
    if len(user) == 0:
        abort(404)

    if request.method == 'GET':
        return user[0].to_dict()

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.get_json().items():
            if k not in ('id', 'created_at', 'updated_at', 'email'):
                setattr(user[0], k, v)
        storage.save()
        return jsonify(user[0].to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(user[0])
        storage.save()
        return {}, 200
