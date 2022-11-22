#!/usr/bin/python3
""" view for State objects that handles all default RESTFul API actions """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route(
    '/users', methods=['GET'], strict_slashes=False,
)
def get_users():
    """ Retrieves all User objects """
    users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(users)


@app_views.route(
    '/users/<user_id>', methods=['GET'],
    strict_slashes=False
)
def getUserId(user_id):
    """ Retrieves a User object by id """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
    '/users/<user_id>', methods=['DELETE'],
    strict_slashes=False
)
def deleteUserId(user_id):
    """ Delete user object by id """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def newUser():
    """ Returns the new User """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in request.get_json():
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in request.get_json():
        return jsonify({'error': 'Missing password'}), 400
    new = request.get_json()
    obj = User(**new)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route(
    '/users/<user_id>', methods=['PUT'],
    strict_slashes=False
)
def updateUser(user_id):
    """ Update the User object """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict())
