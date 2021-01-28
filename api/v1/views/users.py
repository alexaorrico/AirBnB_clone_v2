#!/usr/bin/python3
"""amenitys"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.amenity import Amenity
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_users(user_id=None):
    """get users object"""
    if us_id is None:
        ListUsers = []
        for sUsers in storage.all(User).values():
            ListUsers.append(sUsers.to_dict())
        return jsonify(ListUsers)
    elif storage.get(User, users_id):
        return jsonify(storage.get(User, user_id).to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_user(user_id=None):
    """Delete user object"""
    if storage.get(User, user_id):
        storage.delete(storage.get(User, user_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Add User object"""
    if request.get_json() is None:
        abort(400, "Not a JSON")
    elif "name" not in request.get_json().keys():
        abort(400, "Missing name")
    else:
        Create_user = User(**request.get_json())
        storage.save()
    return jsonify(Create_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id=None):
    """Update user object"""
    if storage.get("User", user_id) is None:
        abort(404)
    if request.get_json() is None:
        return "Not a JSON", 400
    for keye, val in request.get_json().items():
        if keye in ["id", "created_at", "updated_at"]:
            pass
        else:
            setattr(storage.get("Amenity", user_id), keye, val)
    storage.save()
    return jsonify(storage.get("Amenity", user_id).to_dict()), 200
