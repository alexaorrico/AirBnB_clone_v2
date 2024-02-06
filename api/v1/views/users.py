#!/usr/bin/python3
"""
Define route for view User
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.user import User
from models import storage


@app_views.route('/users/<string:user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def users(user_id=None):
    """Retrieves a User or All the users"""
    if request.method == 'GET':
        if user_id is not None:
            user = storage.get(User, user_id)
            if user is None:
                abort(404)
            return jsonify(user.to_dict())
        users = storage.all(User)
        users_dicts = [val.to_dict() for val in users.values()]
        return jsonify(users_dicts)

    elif request.method == 'DELETE':
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        elif 'email' not in data:
            return make_response(jsonify({'error': 'Missing email'}), 400)
        elif 'password' not in data:
            return make_response(jsonify({'error': 'Missing password'}), 400)
        else:
            user = User(**data)
            user.save()
            return make_response(jsonify(user.to_dict()), 201)

    elif request.method == 'PUT':
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
        return make_response(jsonify(user.to_dict()), 200)
