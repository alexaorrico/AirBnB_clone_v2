#!/usr/bin/python3
"""Contains all REST actions for user Objects"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """retrieves a list of all user objects"""
    users = storage.all(User)
    return jsonify([val.to_dict() for val in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """retrieves a user objects"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """deletes a user objects"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def new_user():
    """creates a user objects"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.json:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in request.json:
        return make_response(jsonify({"error": "Missing password"}), 400)
    user = User(**request.get_json())
    if user is None:
        abort(404)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates a user objects"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'password' in request.json:
        user.password = request.get_json()['password']
    if 'first_name' in request.json:
        user.first_name = request.get_json()['first_name']
    if 'last_name' in request.json:
        user.last_name = request.get_json()['last_name']
    user.save()
    return jsonify(user.to_dict())
