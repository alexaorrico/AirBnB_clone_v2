#!/usr/bin/python3
"""Flask route for user model"""

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET', 'POST'])
def users():
    """route to return all users"""
    if request.method == "GET":
        users_dict = storage.all(User)
        users_list = [obj.to_dict() for obj in users_dict.values()]
        return jsonify(users_list)

    if request.method == "POST":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        if request_json.get("name") is None:
            abort(400, "Missing name")

        newUser = User(**request_json)
        newUser.save()
        return make_response(jsonify(newUser.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"])
def user(user_id=None):
    """Get, update or delete state with state id"""
    user_obj = storage.get(User, user_id)

    if user_obj is None:
        abort(404, "Not found")

    if request.method == "GET":
        return jsonify(user_obj.to_dict())

    if request.method == "DELETE":
        user_obj.delete()
        storage.save()
        return jsonify({})

    if request.method == "PUT":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        user_obj.update(request_json)
        return make_response(jsonify(user_obj.to_dict()), 200)
