#!/usr/bin/python3
""" Methos API for object Users """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', defaults={'user_id': None},
                 methods=['GET'],
                 strict_slashes=False)
@app_views.route('/users/<path:user_id>')
def get_user(user_id):
    """ Get all or one User object """
    if user_id is None:
        all_users = storage.all(User)
        return jsonify([
            user.to_dict() for user in all_users.values()
            ])

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Delete a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Create a new User object """
    request_user = request.get_json()
    if not request_user:
        abort(400, "Not a JSON")
    if "email" not in request_user:
        abort(400, "Missing email")
    if "password" not in request_user:
        abort(400, "Missing password")
    user = User(**request_user)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """ Update a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    request_user = request.get_json()
    if not request_user:
        abort(400, "Not a JSON")

    for key, value in request_user.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
