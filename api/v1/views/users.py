#!/usr/bin/python3
"""
File that configures the routes of users
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route("/users", strict_slashes=False)
def get_usersfor():
    """
    Route to get users
    """
    list_obj = []
    for val in storage.all("User").values():
        list_obj.append(val.to_dict())
    return jsonify(list_obj)


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_users(user_id):
    """
    Route to get user
    """
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    deletes a User object
    """
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    user_obj.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def post_user():
    """
    Route that create a new User
    """
    if not request.json:
        abort(400, "Not a JSON")
    if 'email' not in request.json:
        abort(400, "Missing email")
    if 'password' not in request.json:
        abort(400, "Missing password")
    obj_request = request.get_json()
    user_obj = User(**obj_request)
    user_obj.save()
    return (jsonify(user_obj.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def put_user(user_id):
    """
    Route that update an User
    """
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, val in request.get_json().items():
        if (key != "id" and key != "email" and
                key != "created_at" and key != "updated_at"):
            setattr(user_obj, key, val)
    user_obj.save()
    return (jsonify(user_obj.to_dict()), 200)
