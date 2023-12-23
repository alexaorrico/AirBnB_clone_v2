#!/usr/bin/python3
"""
    this module contains flask app routes
        flask APP routes:
        methods:
            GET:
                /users:
                    list all Users
                /users/<user_id>:
                    display User dictionary using ID
            DELETE:
                /users/<user_id>:
                    delete a User using ID
            POST:
                /users:
                    creates a new User
            PUT:
                /users/<user_id>:
                    update User object using ID
"""

from api.v1.views import app_views
from flask import abort, jsonify, request

# import User and Storage models
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"])
def get_Users():
    """display all amenities"""
    user_list = []
    [user_list.append(user.to_dict())
     for user in storage.all(User).values()]
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=["GET"])
def get_User(user_id):
    """diplay a User using ID"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    return obj.to_dict()


@app_views.route("/users/<user_id>", methods=["DELETE"])
def remove_User(user_id):
    """delete a User instance using ID"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"])
def create_User():
    """creates a new User instance"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    obj = User(**(request.get_json()))
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_User(user_id):
    """update a User instance using ID"""
    ignore_keys = ["id", "email", "created_at", "updated_at"]
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    [setattr(obj, key, value) for key, value in request.get_json().items()
     if key not in ignore_keys]
    obj.save()
    return jsonify(obj.to_dict()), 200
