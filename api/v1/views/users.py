#!/usr/bin/python3
"""
Views for User
"""
from flask import request, abort, jsonify
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """
    Retrieves the list of all User objects: GET /api/v1/users
    Creates a User: POST /api/v1/users
    """
    if request.method == 'GET':
        list_states = []
        users = storage.all('User').values()
        for user in users:
            list_states.append(user.to_dict())
        return jsonify(list_states), 200

    if request.method == 'POST':
        request_json = request.get_json()
        if not request_json:
            return jsonify(error='Not a JSON'), 400
        if 'email' not in request_json:
            return jsonify(error='Missing email'), 400
        if 'password' not in request_json:
            return jsonify(error='Missing password'), 400
        user = User(**request_json)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def user(user_id=None):
    """
    Retrieves the list of all User objects: GET /api/v1/users
    Creates a User: POST /api/v1/users
    """
    if request.method == 'GET':
        user = storage.get('User', user_id)
        if user:
            return jsonify(user.to_dict()), 200
        abort(404)

    if request.method == 'DELETE':
        user = storage.get('User', user_id)
        if user:
            storage.delete(user)
            storage.save()
            return jsonify({}), 200
        abort(404)

    if request.method == 'PUT':
        request_json = request.get_json()
        if not request_json:
            return jsonify(error='Not a JSON'), 400
        user = storage.get('User', user_id)
        if user:
            for key, value in request_json.items():
                if key not in ["__class__", "id", "email",
                               "created_at", "updated_at"]:
                    setattr(user, key, value)
            storage.save()
            return jsonify(user.to_dict()), 200
        abort(404)
