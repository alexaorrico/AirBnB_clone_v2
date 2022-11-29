#!/usr/bin/python3
"""module users
Handles users objects for RestfulAPI
"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route("/users/", methods=["GET"],
                 strict_slashes=False)
def get_users():
    """retrieves list of user objects"""
    all_users = storage.all(User)
    list_users = []
    for user in all_users.values():
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route("/users/<string:user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user_id(user_id):
    """retrieves specific user id"""
    user = storage.get(User, user_id)
    if user is not None:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user_id(user_id):
    """deletes user id object"""
    user = storage.get(User, user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/users/", methods=["POST"],
                 strict_slashes=False)
def post_user():
    """creates user object"""
    if request.get_json() is not None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**request.get_json())
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/user/<string:user_id>", methods=["PUT"],
                 strict_slashes=False)
def put_user(user_id):
    """updates user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.get_json() is not None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in request.get_json().items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
