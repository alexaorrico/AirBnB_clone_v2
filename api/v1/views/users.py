#!/usr/bin/python3
"""function to create the route status"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users')
def users():
    ''' retrieve all users '''
    users = storage.all('User').values()
    return jsonify(list(map(lambda u: u.to_dict(), users)))


@app_views.route('/users/<user_id>')
def user_id(user_id):
    """get user with his id"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def users_delete(user_id):
    """delete a obj with his id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def users_create():
    """create user"""
    if request.is_json:
        data = request.get_json()
    else:
        msg = "Not a JSON"
        return jsonify({"error": msg}), 400

    if "email" not in data:
        msg = "Missing email"
        return jsonify({"error": msg}), 400

    if "password" not in data:
        msg = "Missing password"
        return jsonify({"error": msg}), 400

    var = User(**data)
    storage.new(var)
    storage.save()
    return jsonify(var.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def users_update(user_id):
    """update user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
    else:
        msg = "Not a JSON"
        return jsonify({"error": msg}), 400

    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, k, v)

    storage.save()
    return jsonify(user.to_dict()), 200
