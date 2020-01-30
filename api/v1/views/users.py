#!/usr/bin/python3
"""Flask app to handle Users API"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'])
def get_users():
    """Return the list of users"""
    users_dict = storage.all("User")
    users_list = [user.to_dict() for user in users_dict.values()]
    return jsonify(users_list)


@app_views.route('users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Return a user"""
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    user_dict = user_obj.to_dict()
    return jsonify(user_dict)


@app_views.route('users/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    """Delete a user and return an empty dict"""
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    user_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def post_new_user():
    """Return the list of users"""
    json_obj = request.get_json()
    if not request.json:
        return jsonify("Not a JSON"), 400
    if 'email' not in json_obj:
        return jsonify("Missing email"), 400
    if 'password' not in json_obj:
        return jsonify("Missing password"), 400
    new_user_obj = User(**json_obj)
    new_user_obj.save()
    new_user = new_user_obj.to_dict()
    return jsonify(new_user), 201


@app_views.route('users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """Update user by id"""
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    json_obj = request.get_json()
    if not request.json:
        return jsonify("Not a JSON"), 400
    ignore = ["id", "update_at", "created_at", "email"]
    for key, value in json_obj.items():
        if key not in ignore:
            setattr(user_obj, key, value)
    user_obj.save()
    updated_user = user_obj.to_dict()
    return jsonify(updated_user), 200
