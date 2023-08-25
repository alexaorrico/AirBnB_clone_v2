#!/usr/bin/python3
"""
Create a new view for User objects that
handles all default RESTFul API actions
"""
from flask import Flask, request, jsonify, abort
from models import storage
from api.v1.views import app_views
from models.user import User

app = Flask(__name__)


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """Retrieves the list of all User objects"""
    all_users = storage.all(User)
    list_users = [user.to_dict() for user in all_users.values()]
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    to_delete = storage.get(User, user_id)
    if to_delete is None:
        abort(404)
    storage.delete(to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User object"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""
    data = request.get_json()
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
