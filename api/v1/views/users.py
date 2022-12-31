#!/usr/bin/python3
''' user.py '''

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def get_users():
    '''Retrieves the list of all User objects'''
    if request.method == "GET":
        users = storage.all(User).values()
        users = [user.to_dict() for user in users]
        return jsonify(users)

    if request.method == "POST":
        if not request.is_json:
            abort(400, description="Not a JSON")

        if "email" not in request.json:
            abort(400, description="Missing email")

        if "password" not in request.json:
            abort(400, description="Missing password")

        user_json = request.get_json()
        user_obj = User(**user_json)
        storage.new(user_obj)
        storage.save()
        return jsonify(user_obj.to_dict()), 201


@app_views.route("/users/<user_id>",
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_user_id(user_id):
    '''Retrieves a User object'''
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)

    if request.method == "GET":
        return jsonify(user_obj.to_dict())

    if request.method == "DELETE":
        storage.delete(user_obj)
        storage.save()
        return jsonify({}), 200

    if request.method == "PUT":
        if not request.is_json:
            abort(400, description="Not a JSON")

        user_json = request.get_json()
        not_needed = ["id", "created_at", "updated_at", "email"]
        for attr, attr_value in user_json.items():
            if attr not in not_needed:
                setattr(user_obj, attr, attr_value)
        user_obj.save()
        return jsonify(user_obj.to_dict()), 200
