#!/usr/bin/python3
"""
module: User api
"""
from api.v1.views import app_views, storage, User
from flask import jsonify, abort, request


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def get_users():
    """ returns all users in JSON format """
    users = [user.to_json() for user in storage.all('User').values()]
    return jsonify(users)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_single_user(user_id):
    """ returns a user object in JSON format """
    try:
        user = storage.get('User', user_id)
        return jsonify(user.to_json())
    except:
        abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """ deletes a user  """
    if user_id is None:
        abort(404)
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200


@app_views.route('/users/',
                 methods=['POST'], strict_slashes=False)
def post_user():
    """ creates a user """
    json_obj = None
    try:
        json_obj = request.get_json()
    except:
        json_obj = None
    if json_obj is None:
        return "Not a JSON", 400

    if 'email' not in json_obj.keys():
        return "Missing email", 400

    if 'password' not in json_obj.keys():
        return "Missing password", 400

    user = User(**json_obj)
    user.save()
    return jsonify(user.to_json()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id=None):
    """ updates a user  """
    if user_id is None:
        abort(404)
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    try:
        response = request.get_json()
    except:
        response = None
    if response is None:
        return "Not a JSON", 400
    for item in ("id", "created_at", "updated_at", "email"):
        response.pop(item, None)
    for k, v in response.items():
        setattr(user, k, v)
    user.save()
    return jsonify(user.to_json()), 200
