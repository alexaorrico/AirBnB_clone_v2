#!/usr/bin/python3
'''Contains the User view for the API.'''
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Retrieves the list of all User objects"""
    users_list = storage.all(User)
    return jsonify([obj.to_dict() for obj in users_list.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a User"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'email' not in request.get_json():
        abort(400, "Missing email")
    if 'password' not in request.get_json():
        abort(400, "Missing password")
    obj = User(**request.get_json())
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(obj, k, v)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200) 
