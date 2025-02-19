#!/usr/bin/python3
""" index routes """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route("/users")
def get_users():
    """get all users"""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route("/users/<user_id>")
def get_user(user_id):
    """get user"""
    res = storage.get(User, user_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """delete user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"])
def create_user():
    """add new user"""
    if request.json is None:
        abort(400, "Not a JSON")
    data = request.get_json()
    if data.get('email') is None:
        return "Missing email", 400
    if data.get('password') is None:
        return "Missing password", 400
    new_user = User(email=request.json['email'],
                    password=request.json['password'])
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """update user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if request.json is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
