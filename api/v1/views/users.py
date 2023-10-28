#!/usr/bin/python3
"""contains all REST actions for State Objects"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def all_users():
    """retrieves a list of all user objects of State"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<id>', methods=['GET'], strict_slashes=False)
def get_user(id):
    """retrieves a user objects"""
    user = storage.get(User, id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(id):
    """deletes a user objects"""
    user = storage.get(User, id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def new_user():
    """creates a city objects"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.json:
        return make_response(jsonify({"error": "Missing email"}, 400))
    if 'password' not in request.json:
        return make_response(jsonify({"error": "Missing password"}), 400)
    data = request.get_json()
    user = User(**data)
    if user is None:
        abort(404)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<id>', methods=['PUT'], strict_slashes=False)
def update_user(id):
    """updates a user objects"""
    user = storage.get(User, id)
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
    return jsonify(user.to_dict()), 200
