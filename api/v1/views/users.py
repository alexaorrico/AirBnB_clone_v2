#!/usr/bin/python3
"""

"""


from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ """
    users = storage.all(User).values()

    users_list = [user.to_dict() for user in users]

    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """"""
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')

    if 'email' not in data:
        abort(400, description='Missing email')

    if 'password' not in data:
        abort(400, description='Missing password')

    user = User(**data)
    user.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)

    storage.save()

    return make_response(jsonify(user.to_dict()), 200)
