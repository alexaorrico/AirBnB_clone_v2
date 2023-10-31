#!/usr/bin/python3
"""Flask route for amenity model"""

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<users_id>", strict_slashes=False,
                 methods=["GET"])
def new_user(user_id=None):
    """showing all  the user with id"""
    user_list = []
    if user_id is None:
        objs = storage.all(User).values()
        for new in objs:
            user_list.append(new.to_dict())
        return jsonify(user_list)
    else:
        res = storage.get(User, user_id)
        if res is None:
            abort(404)
        return jsonify(res.to_dict())


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def new_users():
    """a new amenity"""
    request_json = request.get_json(force=True, silent=True)
    if not request_json:
        abort(400, "Not a JSON")
    if "name" not in request_json:
        abort(400, "Missing name")
    newUser = user(**request_json)
    newUser.save()
    return jsonify(newUser.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["DELETE"])
def deleting_user(user_id):
    """deleting user"""
    new_obj = storage.get(User, user_id)
    if new_obj is None:
        abort(404)
    storage.delete(new_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["PUT"])
def user_updt(user_id):
    """updating the user"""
    new_obj = storage.get(User, user_id)
    if new_obj is None:
        abort(404)
    request_json = request.get_json(force=True, silent=True)
    if not request_json:
        abort(400, "Not a JSON")
    new_obj.name = request_json.get("name", new_obj.name)
    new_obj.save()
    return jsonify(new_obj.to_dict()), 200
