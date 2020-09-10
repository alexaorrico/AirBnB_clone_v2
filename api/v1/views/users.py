#!/usr/bin/python3
""" Amenity """

from flask import jsonify, request, abort
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=["GET", "POST"],
                 strict_slashes=False)
def list_users():
    """Retrieves the list of all Users objects"""
    if request.method == "GET":
        users = storage.all("User")
        all_users = []
        for key in users.values():
            all_users.append(key.to_dict())
        return jsonify(all_users)
    if request.method == "POST":
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        if "email" not in response:
            abort(400, "Missing email")
        if "password" not in response:
            abort(400, "Missing password")
        new_user = User(**response)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def user(user_id):
    """ Manipulate an specific User """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if request.method == "GET":
        return jsonify(user.to_dict())
    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        for key, value in response.items():
            if key != "id" and key != "created_at" and key != "updated_at"\
                    and key != "email" and hasattr(user, key):
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
