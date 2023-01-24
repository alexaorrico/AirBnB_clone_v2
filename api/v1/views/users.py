#!/usr/bin/python3
""" user view """
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.user import User
from models.base_model import BaseModel


@app_views.route('/users', methods=["GET", "POST"],
                 strict_slashes=False)
def get_all_users():
    """ retrieves all user objects """
    all_users = []
    users = storage.all(User).values()
    for user in users:
        all_users.append(user.to_dict())
    return jsonify(all_users), 200


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_get_user_by_id(user_id):
    """Getting individual users by their ids"""
    user = storage.get('User', user_id)

    if user is None:  # if user_id is not linked to any user obj
        abort(404)  # then, raise 404 error
    else:
        return jsonify(user), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a User,"""
    body = request.get_json()  # transfrom the HTTP body request to dict
    if not body:  # if HTTP body req is  not a valid JSON
        abort(400, {"Not a JSON"})  # raise 400 err with the message Not a JSON
    if 'email' not in body:  # if the dict doesn't contain the key email
        abort(400, {"Missing email"})  # raise err and message
    if 'password' not in body:  # if the dict doesn't contain the key passwd
        abort(400, {"Missing password"})  # raise err and message
    objects = User()
    for key, value in body.items():
        setattr(objects, key, value)
    storage.new(objects)
    storage.save()
    return jsonify(objects.to_dict()), 201  # returns new User


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updating a user object"""
    body = request.get_json()
    if not body:
        abort(400, {"Not a JSON"})
    user = storage.get('User', user_id)
    if user is None:  # if user_id is not linked to any User object
        abort(404)
    for key, value in body.items():  # update User obj with key-val pairs
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200  # return User obj


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_by_id(user_id):
    """Deleting a User object by its id"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    else:
        user.delete()
        del user
    return jsonify({}), 200  # returns an empty dict with status code 200
