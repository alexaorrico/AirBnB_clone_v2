#!/usr/bin/python3
"""Import User module"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    allUsers = storage.all(User).values()
    allUsersList = []
    for user in allUsers:
        allUsersList.append(user.to_dict())
    return jsonify(allUsersList)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get an user with an id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete an user with id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('users', methods=['POST'], strict_slashes=False)
def post_user():
    """creates an user"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    data = request.get_json()
    newUser = User(**data)
    newUser.save()
    return make_response(jsonify(newUser.to_dict()), 201)


@app_views.route('users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updets a User"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'email', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
