#!/usr/bin/python3
"""
Module defines view for User objects that handles all default
RESTFUL API actions.
"""
from models import storage
from models.user import User
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieves all User objects """
    user_list = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ Retrieves User object by user_id """
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)

    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes User object by user_id """
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)

    storage.delete(user_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates User object """
    try:
        data = request.get_json()
        if 'email' not in data or 'password' not in data:
            abort(400, description='Missing name')
    except BadRequest:
        abort(400, description='Not a JSON')

    user_obj = User(**data)
    storage.new(user_obj)
    storage.save()

    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ Updates User object by user_id """
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)

    try:
        data = request.get_json()
    except BadRequest:
        abort(400, description='Not a JSON')

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user_obj, key, value)

    storage.save()

    return jsonify(user_obj.to_dict()), 200
