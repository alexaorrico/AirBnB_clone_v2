#!/usr/bin/python3

""" comment
"""

from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def all_users():
    """
    Return list of the all users
    """
    users_list = []
    users_obj = storage.all("User")
    for _, value in users_obj.items():
        users_list.append(value.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>')
def user(user_id):
    """
    Return a user with the id
    """
    user = storage.get("User", user_id)
    if user is not None:
        return jsonify(user.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    """
    Delete a user with id
    """
    user = storage.get("User", user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """
    Create a new object user
    """
    if not request.get_json():
        return make_response(jsonify({"error": 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({"error": 'Missing password'}), 400)
    user = request.get_json()
    new_user = User(**user)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update a user by id
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    params = request.get_json()
    skip = ['id', 'email', 'created_at', 'updated_at']
    for key, value in params.items():
        if key not in skip:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict())


@app_views.errorhandler(404)
def page_not_found(error):
    """
    Handle 404 error
    """
    return jsonify({"error": "Not found"}), 404
