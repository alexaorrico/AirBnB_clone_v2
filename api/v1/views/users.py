#!/usr/bin/python3
"""View for City objects that handles all default RestFul API"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_all_users():
    """Retrieves the list of all User objects"""
    list_users = storage.all(User).values()
    new_list = []
    for value in list_users:
        new_list.append(value.to_dict())
    return (jsonify(new_list))


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """Retrieves User object"""
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    return (jsonify(user_obj.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete users obj by id"""
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    else:
        user_obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User - POST"""
    req_user = request.get_json()
    if not req_user:
        abort(400, "Not a JSON")
    if 'email' not in req_user:
        abort(400, "Missing email")
    if 'password' not in req_user:
        abort(400, "Missing password")
    new_user = User(**req_user)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user_obj = storage.get("User", user_id)
    req = request.get_json()

    if user_obj is None:
        abort(404)
    if not req:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in req.items():
        if attr not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_obj, attr, val)
    storage.save()
    return jsonify(user_obj.to_dict())
