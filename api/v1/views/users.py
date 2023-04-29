#!/usr/bin/python3
"""creates a new view for users that handles all Rest Api actions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def get_user(user_id=None):
    """retrieves the list of all user objects"""
    users = storage.all(User)
    if not user_id:
        # uses the '/users/ routes
        if request.method == 'GET':
            user_list = []
            for user in users.values():
                user_list.append(user.to_dict())
            return jsonify(user_list)
        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                abort(400, 'Not a JSON')
            if not data.get('email'):
                abort(400, 'Missing email')
            if not data.get('password'):
                abort(400, 'Missing password')
            new_obj = User(**data)
            new_obj.save()
            return jsonify(new_obj.to_dict()), 201
    else:
        # uses the '/users/<user_id>' route
        user_obj = storage.get(User, user_id)
        if not user_obj:
            abort(404)
        if request.method == 'GET':
            return jsonify(user_obj.to_dict())
        elif request.method == 'DELETE':
            storage.delete(user_obj)
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                abort(400, 'Not a JSON')
            user_obj.name = data.get('name')
            user_obj.save()
            return jsonify(user_obj.to_dict()), 200
