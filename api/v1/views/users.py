#!/usr/bin/python3
"""users views"""
from models.user import User
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/users/<user_id>', methods=['GET'])
@app_views.route('/users', defaults={'user_id': None}, methods=['GET'])
def retrives_user(user_id):
    """Retrives the list of all users"""
    if user_id is None:
        return jsonify([
            user.to_dict() for user in storage.all(User).values()])

    if storage.get(User, user_id) is None:
        abort(404)

    return jsonify(storage.get(User, user_id).to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    users.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """creates a new user"""
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    if 'email' not in json_data:
        abort(400, 'Missing email')
    if 'password' not in json_data:
        abort(400, 'Missing password')
    user = User(**json_data)
    user.save()
    # return a tuple default(data, status)
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """update a user"""
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for key, values in json_data.items():
        if key not in ('id', 'created_at', 'updated_at', 'email'):
            setattr(user, key, values)
    user.save()
    return jsonify(user.to_dict()), 200
