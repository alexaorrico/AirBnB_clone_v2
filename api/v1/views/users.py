#!/usr/bin/python3
"""
 view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users')
def get_users():
    """Retrieves the list of all User objects """
    users = [
        amn.to_dict()
        for amn in storage.all(User).values()
    ]
    return jsonify(users)
    return jsonify(users)


@app_views.route('/users/<user_id>')
def get_user(user_id):
    """Retrieves a User object based on user_id, raises a 404 error
    if user_id is not linked to any User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User Object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def add_user():
    """creates a User"""
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    if 'email' not in request.get_json():
        return ("Missing email\n", 400)
    if 'password' not in request.get_json():
        return ("Missing password\n", 400)
    request_data = request.get_json()
    new_user = User(**request_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """updates a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
        # return (jsonify(error="Not a JSON"), 400)
    request_data = request.get_json()
    request_data.pop('id', None)
    request_data.pop('email', None)
    request_data.pop('created_at', None)
    request_data.pop('updated_at', None)
    for key in request_data:
        setattr(user, key, request_data[key])
    user.save()
    return jsonify(user.to_dict()), 200
