#!/usr/bin/python3
"""
Handle apis from users
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    get user information for all users in a users list
    """
    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """
    get user information for specified user
    based on the id provided
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    deletes a user based on its user_id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return (jsonify({}))


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_a_user():
    """
    create a new user
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],strict_slashes=False)
@swag_from('documentation/amenity/put.yml', methods=['PUT'])
def post_amenity(amenity_id):
    """
    update an amenity
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())

