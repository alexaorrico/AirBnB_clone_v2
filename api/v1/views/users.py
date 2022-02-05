#!/usr/bin/python3
""" user view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.user import User
from models.base_model import BaseModel


@app_views.route('/users', methods=["GET", "POST"],
                 strict_slashes=False)
def get_all_users():
    """ retrieves all user objects """
    output = []
    users = storage.all(User).values()
    if request.method == "GET":
        for user in users:
            output.append(user.to_dict())
        return (jsonify(output))
    if request.method == "POST":
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'email' not in request.json:
            abort(400, description="Missing email")
        if 'password' not in request.json:
            abort(400, description="Missing password")
        user = User(**data)
        user.save()
        return (jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def get_a_user(user_id):
    """ retrieves one unique user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == "GET":
        output = user.to_dict()
        return (jsonify(output))
    if request.method == "PUT":
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return (jsonify(user.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        result = make_response(jsonify({}), 200)
        return result
