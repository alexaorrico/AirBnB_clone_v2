#!/usr/bin/python3
""" state view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.user import User
from models.base_model import BaseModel


@app_views.route('/users', methods=["GET", "POST"], strict_slashes=False)
def get_users():
    """get all instances of user"""
    if request.method == "GET":
        response = []
        users = storage.all(User).values()
        for user in users:
            response.append(user.to_dict())
        return (jsonify(response))

    if request.method == "POST":
        """post a new instance"""
        new_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'email' not in request.json:
            abort(400, description="Missing email")
        if 'password' not in request.json:
            abort(400, description="Missing password")
        user = User(**new_data)
        user.save()
        return (jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["GET", "PUT"],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """get, update an instance of user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == "GET":
        response = user.to_dict()
        return (jsonify(response))
    if request.method == "PUT":
        new_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in new_data.items():
            setattr(user, key, value)
        user.save()
        return (jsonify(user.to_dict()), 200)


@app_views.route('/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """delete an instance of amenity"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        response = make_response(jsonify({}), 200)
        return response
