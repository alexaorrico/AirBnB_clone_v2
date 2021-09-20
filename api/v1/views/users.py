#!/usr/bin/python3
"""User objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
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
def get_user_id(user_id):
    """ get user for id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_user(user_id=None):
    """ Deletes state by id """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """ Creates new user """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    new_user = User(**data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id", strict_slashes=False, methods=["PUT"])
def update_user(user_id=None):
    """ Updates user """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
