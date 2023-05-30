#!/usr/bin/python3
"""A new view for User object that handles all default RESTFul API actions"""

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/users', strict_slashes=False,
                 methods=['GET', 'POST'])
def users():
    """Retrieves the list of all User objects"""
    if request.method == 'GET':
        return jsonify([user.to_dict() for user in
                        storage.all(User).values()])

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'email' not in request.json:
            abort(400, 'Missing email')
        if 'password' not in request.json:
            abort(400, 'Missing password')
        new_user = User(**request.get_json())
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def users_id(user_id):
    """Retrieves a User object using user id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.json.items():
            if k not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, k, v)
        user.save()
        return make_response(jsonify(user.to_dict()), 200)
