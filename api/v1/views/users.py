#!/usr/bin/python3
""" methods to handle all default RESTFul API actions for Users """

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieves a specific user"""
    dic_users = storage.all(User)
    return jsonify([obj.to_dict() for obj in dic_users.values()])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieves a single User object by id"""
    user_d = storage.get(User, user_id)

    if user_d is None:
        abort(404)

    # return the user object
    return jsonify(user_d.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User obje"""
    user = storage.get(User, user_id)

    # check if user obj exists
    if user is None:
        abort(404)

    # delete the user obj
    user.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """creates a User obj"""
    new_user_d = request.get_json()

    if not new_user_d:
        abort(400, "Not a JSON")
    elif "email" not in new_user_d.keys():
        abort(400, "Missing email")
    elif "password" not in new_user_d.keys():
        abort(400, "Missing password")
    else:
        new_user_d = User(**new_user_d)
        new_user_d.save()

    return make_response(jsonify(new_user_d.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """updates  user obj"""

    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    new_user_d = request.get_json()

    if not new_user_d:
        abort(400, "Not a JSON")
    else:
        # update the user object
        for k, v in new_user_d.items():
            if k not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, k, v)
        storage.save()

    # return the updated user
    return jsonify(user.to_dict())
