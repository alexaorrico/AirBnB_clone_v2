#!/usr/bin/python3
"""index """

from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User


@app_views.route("/users", methods=['GET', 'POST'])
def users_without_id():
    """Create a new User or return all the users"""
    if request.method == 'GET':
        users_list = []
        users_dict = storage.all(User)
        for user in users_dict.values():
            users_list.append(user.to_dict())
        return jsonify(users_list)

    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, "Not a JSON")
        if json.get('email') is None:
            abort(400, "Missing email")
        if json.get('password') is None:
            abort(400, "Missing password")
        user = User(**json)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['GET', 'PUT', 'DELETE'])
def users_with_id(user_id=None):
    """Perform READ UPDATE DELETE operations on a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        user.delete()
        del user
        return jsonify({})

    if request.method == 'PUT':
        json = request.get_json()
        if json is None:
            abort(400, "Not a JSON")
        json.pop("email", None)
        user.update(**json)
        return jsonify(user.to_dict()), 200
