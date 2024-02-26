#!/usr/bin/python3
"""Create a new view for User objects, this view can handle RESTful API"""
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=["GET", "POST"],
                 strict_slashes=False)
def get_available_users():
    """
    function to get all available users
    """
    output_list = []
    all_users = storage.all(User).values()
    if request.method == "GET":
        for user in all_users:
            output_list.append(user.to_dict())
        return (jsonify(output_list))
    if request.method == "POST":
        user_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'email' not in request.json:
            abort(400, description="Missing email")
        if 'password' not in request.json:
            abort(400, description="Missing password")
        user = User(**user_data)
        user.save()
        return (jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def get_single_user(user_id):
    """
    retrieves one unique user object, with its ID well defined
    """
    defined_user = storage.get(User, user_id)
    if defined_user is None:
        abort(404)
    if request.method == "GET":
        user_output = defined_user.to_dict()
        return (jsonify(user_output))
    if request.method == "PUT":
        user_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in user_data.items():
            setattr(defined_user, key, value)
        defined_user.save()
        return (jsonify(defined_user.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(defined_user)
        storage.save()
        result = make_response(jsonify({}), 200)
        return result
