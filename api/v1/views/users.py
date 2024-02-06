#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.user import User
from models.base_model import BaseModel


@app_views.route("/users", methods=["GET", "POST"],
                 strict_slashes=False)
def get_users():
    """Get Users"""
    res = []
    users = storage.all(User).values()
    if request.method == "GET":
        for user in users:
            res.append(user.to_dict())
        return jsonify(res)
    if request.method == "POST":
        if not request.json:
            abort(400, description="Not a JSON")
        if 'email' not in request.json:
            abort(400, description="Missing email")
        if 'password' not in request.json:
            abort(400, description="Missing password")
        new_user = User(**request.json)
        new_user.save()
        return (jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<int:id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=True)
def get_user(id):
    """Get User"""
    user = storage.get(User, id)
    if user is None:
        abort(404)
    if request.method == "GET":
        return jsonify(user.to_dict())
    if request.method == "PUT":
        if not request.json:
            abort(400, description="Not a JSON")
        for key, value in request.json.items():
            setattr(user, key, value)
        user.save()
        return (jsonify(user.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return (jsonify({}), 200)
