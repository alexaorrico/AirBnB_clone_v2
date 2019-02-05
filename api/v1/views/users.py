#!/usr/bin/python3
"""Module to create a new view for User objects"""

from flask import jsonify, Flask, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes = False)
def get_users():
    """Retrieves the list of all User objects"""
    all_users = storage.all('User')
    my_list = []
    for value in all_users.values():
        my_list.append(value.to_dict())
    return (jsonify(my_list))

@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes = False)
def get_user_by_user_id(user_id):
    """Retrieves an User object by user_id"""
    user = storage.get('User', str(user_id))
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes = False)
def delete_user_by_id(user_id):
    """Deletes an User object by ID"""
    user = storage.get('User', str(user_id))
    if user is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'],
                 strict_slashes = False)
def create_users():
    """Post an User object"""
    data = request.get_json()
    if not data:
        abort(400)
        abort(Response("Not a JSON"))
    if 'name' not in data:
        abort(400)
        abort(Response("Missing name"))
    new_user = User(**data)
    return jsonify(new_user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes = False)
def put_user(user_id):
    """Put an User object"""
    data = request.get_json()
    if not data:
        abort(400)
        abort(Response("Not a JSON"))
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 200
