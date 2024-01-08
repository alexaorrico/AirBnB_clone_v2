#!/usr/bin/python3
"""Amenity view"""
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/users', strict_slashes=False)
def get_users():
    """Retrieves the list of all user objects"""
    from models import storage
    from models.user import User
    users = storage.all(User)
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """Retrieves a user object"""
    from models import storage
    from models.user import User
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object"""
    from models import storage
    from models.user import User
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a user"""
    from models import storage
    from models.user import User
    from flask import request

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.get_json():
        return jsonify({"error": "Missing password"}), 400

    user = User(**request.get_json())
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a user object"""
    from models import storage
    from models.user import User
    from flask import request
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
