#!/usr/bin/python3
""" view for user """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_users(user_id=None):
    """ retrieves all users """
    if not user_id:
        users = storage.all(User)
        list_user = []
        for user in users.values():
            list_user.append(user.to_dict())
        return jsonify(list_user)
    else:
        user = storage.get(User, user_id)
        if user is None:
            return abort(404)
        return user.to_dict()


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ deletes user """
    if user_id is None:
        return abort(404)
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ post to users """
    if not request.json:
        return 'Not a JSON', 400
    if 'email' not in request.json:
        return 'Missing email', 400
    if 'password' not in request.json:
        return 'Missing password', 400
    body = request.get_json()
    new_user = User(**body)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ update user """
    if user_id is None:
        return abort(404)
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    if not request.json:
        return 'Not a JSON', 400
    body = request.get_json()
    for key, value in body.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at' or\
                key == 'email':
            continue
        setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
