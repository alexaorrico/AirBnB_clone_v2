#!/usr/bin/python3
"""RESTFul API"""
from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_all_users():
    """list of all User"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users]), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """new User"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    nw_user = User(**data)
    storage.new(nw_user)
    storage.save()
    return jsonify(nw_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """get User"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_by_id(user_id):
    """ delete User """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_by_id(user_id):
    """update User"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ig_key = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ig_key:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
