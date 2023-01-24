#!/usr/bin/python3
""" This module contains the users view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def handle_users():
    """ This function handles the users route """
    if request.method == 'GET':
        users = storage.all('User').values()
        return jsonify([user.to_dict() for user in users])
    elif request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        elif 'email' not in request.json:
            abort(400, 'Missing email')
        elif 'password' not in request.json:
            abort(400, 'Missing password')
        user = User(**request.json)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_user(user_id):
    """ This function handles the user route """
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for key, value in request.json.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
