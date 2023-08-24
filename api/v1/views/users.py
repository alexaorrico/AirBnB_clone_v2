#!/usr/bin/python3
"""users script"""

from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def list_all_users():
    '''Retrieves a list of all Users objects'''
    list_all_users = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(list_all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object by ID"""
    user = storage.get(User, user_id)
    if user is not None:
        return jsonify(user.to_dict())
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object by ID"""
    user = storage.get(User, user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user"""
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request_data:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request_data:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    new_user = User(**request_data)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object by ID"""
    user = storage.get(User, user_id)
    if user is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
