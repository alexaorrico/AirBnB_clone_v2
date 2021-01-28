#!/usr/bin/python3
"""handles user route requests"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/users', strict_slashes=False, methods=[
    'POST', 'GET'])
@app_views.route('/users/<user_id>', strict_slashes=False, methods=[
    'PUT', 'GET', 'DELETE'])
def amenities(user_id=None):
    """handles HTTP requests related to users"""
    if user_id is None:
        # /users GET method
        if request.method == 'GET':
            list_users = storage.all(User)
            return jsonify([user.to_dict() for user in list_users.values()])

        # /users POST method
        if request.method == 'POST':
            new_json = request.get_json(silent=True)
            if new_json is None:
                abort(400, 'Not a JSON')
            if 'email' not in new_json:
                abort(400, 'Missing email')
            if 'password' not in new_json:
                abort(400, 'Missing password')
            new_user = User(**new_json)
            new_user.save()
            return jsonify(new_user.to_dict()), 201

    else:
        # /users/<user_id> GET method
        if request.method == 'GET':
            user = storage.get(User, user_id)
            if user is not None:
                return jsonify(user.to_dict())
            abort(404)

        # /users/<user_id> DELETE method
        if request.method == 'DELETE':
            user = storage.get(User, user_id)
            if user is not None:
                user.delete()
                storage.save()
                return jsonify({}), 200
            abort(404)

        # /users/<user_id> PUT method
        if request.method == 'PUT':
            user = storage.get(User, user_id)
            if user is None:
                abort(404)
            new_json = request.get_json(silent=True)
            if new_json is None:
                abort(400, 'Not a JSON')
            for k, v in new_json.items():
                if k not in ['id', 'email', 'created_at', 'updated_at']:
                    setattr(user, k, v)
            user.save()
            return jsonify(user.to_dict()), 200
