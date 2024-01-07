#!/usr/bin/python3
""" Views for User objects """
from api.v1.views import user_view
from flask import jsonify, abort, request
from models import storage
from models.user import User
import hashlib


@user_view.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """ Retrieves the list of User objects """
    r_user = storage.all(User)
    return jsonify([obj.to_dict() for obj in d_users.values()])


@user_view.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """ Get User based on user_id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@user_view.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 201


@user_view.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates a User object """
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if "email" not in new_user:
        abort(400, "Missing email")
    if "password" not in new_user:
        abort(400, "Missing password")

    user = User(**new_user)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@user_view.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ Updates a user object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data_request = request.get_json()
    if not data_request:
        abort(400, "Not a JSON")

    for key, value in data_request.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
