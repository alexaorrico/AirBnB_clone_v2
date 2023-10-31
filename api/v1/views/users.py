#!/usr/bin/python3

"""view for User object that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    Users = storage.all(User).values()
    return jsonify([user.to_dict() for user in Users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a User"""
    if not request.get_json():
        abort(400, {'message': 'Not a JSON'})
    if 'email' not in request.get_json():
        abort(400, {'message': 'Missing name'})
    if 'password' not in request.get_json():
        abort(400, {'message': 'Missing password'})
    data = request.get_json()
    user = User(**data)
    user.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User Object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, {'message': 'Not a JSON'})
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return (jsonify(user.to_dict()), 200)
