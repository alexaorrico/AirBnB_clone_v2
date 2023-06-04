#!/usr/bin/python3

"""
a new view for User objects that handles all default RESTFul API actions
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def retrieve_user():
    """
    Retrieves all the users
    """

    user_list = []
    users = storage.all(User)
    for user in users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def retrieve_user_using_userid(user_id):
    """
    REtrieves the user using the user id
    Raises a 404 error if the user_id isnt linked to a user
    """

    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user_using_userid(user_id):
    """
    Deletes a user using the user id
    Raises a 404 error If the user_id is not linked to any User object
    Returns an empty dictionary with the status code 200
    """

    user = storage.get(User, user_id)
    if user:
        user.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """
    Posts a new user
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    user_data = request.get_json()
    user = User()
    for key, value in user_data.items():
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates a user using the user id
    Returns a 404 error if the user id is not linked to any user
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user = storage.get(User, user_id)
    keys_ignore = ["id", "updated_at", "created_at"]
    if user:
        for key, value in request.get_json().items():
            if key not in keys_ignore:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    abort(404)
