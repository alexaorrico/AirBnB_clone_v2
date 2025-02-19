#!/usr/bin/python3
""" The State Object view
"""

from flask import jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False)
def get_users():
    """ Retrieves users from storage
    """
    retrieved_users = []
    user_objects = storage.all(User)
    for state in user_objects.values():
        retrieved_users.append(state.to_dict())
    return jsonify(retrieved_users), 200


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user_by_id(user_id):
    """ Retrieves one user from storage based on the id
    """
    try:
        return jsonify(storage.get(User, user_id).to_dict()), 200
    except Exception:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """ Deletes the user from storage by its given id
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Adds a new user to storage
    """
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if 'email' not in body:
        abort(400, 'Missing name')
    if 'password' not in body:
        abort(400, 'Missing password')
    new_user = User(**body)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ Modifies the attributes of a user if they are not dates or id
    """
    user = storage.get(User, user_id)
    if user:
        body = request.get_json()
        if body is None:
            abort(400, 'Not a JSON')
        for key, value in body.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
