#!/usr/bin/python3
""" Configures RESTful api for the users route """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def users():
    """ configures the user route """

    if request.method == "GET":
        users = storage.all(User)
        users_dict = [user.to_dict() for user in users.values()]

        return jsonify(users_dict)
    else:
        try:
            json_dict = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        try:
            email = json_dict["email"]
        except KeyError:
            abort(400, "Missing email")

        try:
            password = json_dict["password"]
        except KeyError:
            abort(400, "Missing password")

        new_user = User()
        new_user.email = email
        new_user.password = password
        new_user.first_name = json_dict.get("first_name")
        new_user.last_name = json_dict.get("last_name")

        storage.new(new_user)
        storage.save()

        return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def users_id(user_id):
    """ configures the users/<user_id> route """

    user = storage.get("User", user_id)

    if not user:
        abort(404)

    if request.method == "GET":
        return jsonify(user.to_dict())
    elif request.method == "DELETE":
        storage.delete(user)
        storage.save()

        return jsonify({}), 200
    else:
        try:
            json_dict = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        keys_to_ignore = ["id", "email", "created_at", "updated_at"]
        for key, val in json_dict.items():
            if key not in keys_to_ignore:
                setattr(user, key, val)

        storage.new(user)
        storage.save()

        return jsonify(user.to_dict()), 200
