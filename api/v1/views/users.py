#!/usr/bin/python3
"""creates a new view for users that handles all Rest Api actions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
import hashlib
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
            ignore_keys = ["id", "email", "created_at", "updated_at"]
            for key in data.keys():
                if key not in ignore_keys:
                    if key == 'password':
                        hashed = hashlib.new('md5')
                        hashed.update(bytes("{}".format(data.get(key)),
                                      encoding='utf-8'))
                        data[key] = hashed.hexdigest()
                    setattr(user_obj, key, data.get(key))
            user_obj.save()
            return jsonify(user_obj.to_dict()), 200
