#!/usr/bin/python3
"""RESTful API view to handle actions for 'User' objects"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def users_routes():
    """
    GET: Retrieves the list of all User objects
    POST: Creates a User object
    """
    if request.method == "GET":
        users = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(users)

    if request.method == "POST":
        in_data = request.get_json(silent=True)
        if in_data is None or not isinstance(in_data, dict):
            return 'Not a JSON\n', 400

        for key in ["email", "password"]:
            val = in_data.get(key)
            if val is None:
                return "Missing {}}\n".format(key), 400

        user = User(**in_data)
        user.save()
        return user.to_dict(), 201


@app_views.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def user_id_routes(user_id):
    """
    GET: Retrieves the User where id == user_id
    PUT: Updates the User that has id == user_id
    PUT: Deletes the User that has id == user_id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == "GET":
        return jsonify(user.to_dict())

    elif request.method == "PUT":
        in_data = request.get_json(silent=True)
        if in_data is None or not isinstance(in_data, dict):
            return 'Not a JSON\n', 400

        for key, val in in_data.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, key, val)
        user.save()
        return user.to_dict(), 200

    elif request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
