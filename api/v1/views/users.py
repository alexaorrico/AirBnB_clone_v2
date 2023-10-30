#!/usr/bin/python3
"""this view hundles states endpoints"""
from flask import abort
from api.v1.views import app_views
from flask import jsonify
from flask import request
from flask import make_response
from models.user import User
from models import storage


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """gets all users instances"""
    d_users = storage.all(User)
    users = []
    for user in d_users.values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """gets user with the given id"""
    d_user = storage.get(User, user_id)
    if d_user:
        return jsonify(d_user.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """deletes user with the given id"""
    d_user = storage.get(User, user_id)
    if d_user:
        storage.delete(d_user)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """create new user with the supplied data"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if "password" not in data:
        return make_response(jsonify({"error": "Missing password"}), 400)
    if "email" not in data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    new = User(**data)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """updates user with supplied id"""
    d_user = storage.get(User, user_id)

    if not d_user:
        abort(404)

    if request.get_json():
        data = request.get_json()
        for k, v in data.items():
            if k not in ["id", "email", "created_at", "updated_at"]:
                setattr(d_user, k, v)
        d_user.save()
        return make_response(jsonify(d_user.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)
