#!/usr/bin/python3
""" User """
import json
from models import storage
from flask import jsonify, abort, request, make_response
from models.user import User
from api.v1.views import app_views


@app_views.route("/users", methods=['GET', 'POST'], strict_slashes=False)
def users():
    """ Retrieves the list of all User objects or create one"""
    if request.method == 'GET':
        list_users = []
        users = storage.all(User).values()
        for user in users:
            list_users.append(user.to_dict())
        return jsonify(list_users)

    if request.method == 'POST':
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        if response.get("email") is None:
            abort(400, "Missing email")
        if response.get("password") is None:
            abort(400, "Missing password")

        new = User(**response)
        new.save()
        return make_response(jsonify(new.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def users_id(user_id):
    """ Do some methods on a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({})

    elif request.method == 'PUT':
        ignore = ["id", "created_at", "updated_at"]
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        for key, value in response.items():
            if key not in ignore:
                setattr(user, key, value)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
