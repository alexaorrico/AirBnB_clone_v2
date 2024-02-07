#!/usr/bin/python3
"""
Define route for view User
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users/<string:user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def users(user_id=None):
    """Retrieves a User or All the users"""
    user = storage.get(User, user_id)

    if request.method == 'GET':
        if user_id is not None:
            if user is None:
                abort(404)
            return jsonify(user.to_dict())
        users = storage.all(User)
        users_dicts = [val.to_dict() for val in users.values()]
        return jsonify(users_dicts)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'email' not in data:
            abort(400, 'Missing email')
        if 'password' not in data:
            abort(400, 'Missing password')

        user = User(**data)
        user.save()
        return jsonify(user.to_dict()), 201

    if user is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        user = storage.get(User, user_id)
        if user is None:
            abort(404)

        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
