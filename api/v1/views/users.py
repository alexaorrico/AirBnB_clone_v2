#!/usr/bin/python3
"""
module for CRUD User object
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def get_all_users():
    """ retrieve the list of users"""
    all_user = storage.all(User).values()
    users = [u.to_dict() for u in all_user]
    return jsonify(users)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """retrieve user using param id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """ remove user from storage"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ create new user """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")
    obj_user = User(**data)
    obj_user.save()
    return jsonify(obj_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ update user based on user_id"""
    ref_obj_user = storage.get(User, user_id)
    if not ref_obj_user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key in data:
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            # ref_obj_state.__dict__[key] = data[key]
            setattr(ref_obj_user, key, data[key])
    storage.save()
    return jsonify(ref_obj_user.to_dict()), 200
