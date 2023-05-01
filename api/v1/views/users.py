#!/usr/bin/python3

""" Handles all restful API actions for User"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from models import storage


@app_views.route('/users',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def users(user_id=None):
    """Retrieves a list of user objects"""

    users_objs = storage.all(User)

    users = [obj.to_dict() for obj in users_objs.values()]
    if not user_id:
        if request.method == 'GET':
            return jsonify(users)
        if request.method == 'POST':
            my_dict = request.get_json()

            if my_dict is None:
                abort(400, 'Not a JSON')
            if my_dict.get("email") is None:
                abort(400, 'Missing email')
            if my_dict.get("password") is None:
                abort(400, 'Missing password')
            new_user = User(**my_dict)
            new_user.save()
            return jsonify(new_user.to_dict()), 201
    else:
        user = storage.get(User, user_id)

        if user is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(user.to_dict())
        if request.method == 'PUT':
            my_dict = request.get_json()

            if my_dict is None:
                abort(400, 'Not a JSON')
            for k, v in my_dict.items():
                setattr(user, k, v)
            user.save()
            return jsonify(user.to_dict()), 200
        if request.method == 'DELETE':
            user.delete()
            storage.save()
            return jsonify({}), 200
