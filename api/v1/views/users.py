#!/usr/bin/python3
""" Object that handles all default RESTFul API actions for users """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """ Retrieves a list of all user objects """
    all_users = storage.all(User).values()
    list_users = []
    for user  in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)

@app_views.route('/users/<user_id>', method='GET', strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get_user(User, user_id)
    if not user:
        abort(404)
    
    storage.delete(user)
    storage.save()

    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates a User """
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = User(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ Updates a User object. """
    user = storage.get_user(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description='Not a JSON')

    ignore = ['id', 'name', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
