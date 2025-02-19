#!/usr/bin/python3
"""
Module that creates a view for User
"""

from flask import jsonify, abort, request
from api.v1.views.__init__ import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def user_index(user_id=None):
    """
    Retrieves a list of all user objects on
    GET /api/v1/users request
    """
    if user_id is None:
        users_obj = list(storage.all(User).values())
        users_list = list(user.to_dict() for user in users_obj)
        return jsonify(users_list)
    else:
        obj = storage.get(User, user_id)
        if obj is not None:
            return jsonify(obj.to_dict())
        else:
            abort(404)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def post_user():
    """
    Posts an User object on
    POST /api/v1/users request
    """
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        abort(400, description='Not a JSON')
    else:
        json = request.get_json()
        if json is None:
            abort(400, description='Not a JSON')
        if 'email' not in json.keys():
            abort(400, description='Missing email')
        elif 'password' not in json.keys():
            abort(400, description='Missing password')
        else:
            obj = User(**json)
            obj_id = obj.id
            obj.save()
            return user_index(obj_id), 201


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """
    Deletes a user object on
    DELETE /api/v1/users/<user_id> request
    """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """
    Replaces a user object on
    PUT /api/v1/users/<user_id> request
    """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)

    else:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            abort(400, description='Not a JSON')
        else:
            json = request.get_json()
            if json is None:
                abort(400, description='Not a JSON')
            for key, value in json.items():
                if key not in ['id', 'email', 'created_at', 'updated_at']:
                    setattr(obj, key, value)
                storage.save()
            return user_index(user_id), 200
