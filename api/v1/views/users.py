#!/usr/bin/python3
"""
module for user views
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """ Retrieves the list of all User objects """
    users = storage.all("User")
    result = []
    for user in users.values():
        result.append(user.to_dict())
    return jsonify(result)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    users = storage.all("User")
    for key in users.keys():
        if key.split('.')[-1] == user_id:
            return jsonify(users.get(key).to_dict())
    abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    users = storage.all("User")
    for key in users.keys():
        if key.split('.')[-1] == user_id:
            storage.delete(users.get(key))
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates a User """
    dic = request.get_json()
    if not dic:
        abort(400, "Not a JSON")
    if not ('email' in dic.keys()):
        abort(400, "Missing email")
    if not ('password' in dic.keys()):
        abort(400, "Missing password")
    user = User(**dic)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ Updates a User object """
    users = storage.all("User")
    user = None
    for key in users.keys():
        if key.split('.')[-1] == user_id:
            user = users.get(key)
    if not user:
        abort(404)
    new_dict = request.get_json()
    if not new_dict:
        abort(400, "Not a JSON")
    for key, value in new_dict.items():
        if key in ('id', 'email', 'created_at', 'updated_at'):
            continue
        else:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
