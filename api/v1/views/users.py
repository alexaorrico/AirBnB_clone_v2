#!/usr/bin/python3
"""User objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def get_user():
    """ return all user objects"""
    users = storage.all(User).values()
    resultado = []

    for user in users:
        resultado.append(user.to_dict())

    return jsonify(resultado)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user_id(user_id=None):
    """ get user for id """
    users = storage.all("User").values()
    resultado = []
    if user_id is not None:
        for user in users:
            if user_id == user.id:
                return jsonify(user.to_dict())
        return abort(404)

    return jsonify(resultado)


@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_user(user_id=None):
    """ Deletes state by id """
    try:
        user = storage.get(User, user_id)

        if user is not None:
            storage.delete(user)
            storage.save()
            return jsonify({}), 200

        abort(404)
    except:
        abort(404)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """ Creates new user """
    try:
        user = request.get_json()

        if user.get("email") is None:
            return jsonify({"error": "Missing email"}), 400
        elif user.get("password") is None:
            return jsonify({"error": "Missing password"}), 400
    except:
        return jsonify({"error": "Not a JSON"}), 400

    new_user = User(**user)
    storage.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id", strict_slashes=False, methods=["PUT"])
def update_user(user_id=None):
    """ Updates user """
    try:
        json = request.get_json()

        if isinstance(json, dict) is False:
            raise Exception(400)
    except:
        return jsonify({"error": "Not a JSON"}), 400

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    att_skip = ["id", "created_at", "updated_at", "email"]
    for key, value in json.items():
        if key not in att_skip:
            setattr(user, key, value)

    user.save()

    return jsonify(user.to_dict()), 200
