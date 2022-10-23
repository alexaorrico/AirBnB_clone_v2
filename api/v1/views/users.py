#!/usr/bin/pythion3
"""Routes for user objects"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route('/users/', method=['GET'], strict_slashes=False)
def get_all_user():
    """return all users in the database"""
    data = storage.all(User)
    new = [value.to_dict() for key, value in data.items()]
    return jsonify(new)


@app_views.route('/users/<user_id>', method=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """return all users"""
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/users/<user_id>', method=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """delete an individual user"""
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', method=['POST'], strict_slashes=False)
def create_user():
    """Create a new user if not exists"""
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif "email" is not args:
        return jsonify({"error": "Missing email"}), 400
    elif "password" is not args:
        return jsonify({"error": "Missing password"}), 400
    obj = User(**args)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 200
