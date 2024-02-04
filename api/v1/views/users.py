#!/usr/bin/python3
""" This module contains a blue print for a restful API that
    works for user objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def post_get_user_obj():
    """ This function contains two http method handler

        GET:
            return the all user objects
        POST:
            create a new user object
    """
    if request.method == 'GET':
        user_objects = storage.all(User)
        user_list = []
        for user in user_objects.values():
            user_list.append(user.to_dict())
        return jsonify(user_list)
    elif request.method == 'POST':
        try:
            user_dict = request.get_json()
        except Exception:
            abort(400, description="Not a JSON")
        if "email" not in user_dict:
            abort(400, description="Missing email")
        if "password" not in user_dict:
            abort(400, description="Missing password")
        new_user = User(**user_dict)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def delete_put_get_user_obj(user_id):
    """ This function contains two http method handler

        GET:
            get the user object with the respective id
        DELETE:
            delete the user object with the respective id
        PUT:
            update the user object with the respective id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    elif request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            user_dict = request.get_json()
            for key, value in user_dict.items():
                if key not in ["id", "created_at", "email"]:
                    setattr(user, key, value)
            user.save()
            return jsonify(user.to_dict()), 200
        except Exception:
            abort(400, description="Not a JSON")
