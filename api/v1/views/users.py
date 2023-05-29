#!/usr/bin/python3
""" Blueprint for User objs that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=["GET"], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=["GET"], strict_slashes=False)
def user(user_id=None):
    """ Retrieves User obj """
    if user_id is None:
        users = storage.all("User")
        my_users = [value.to_dict() for key, value in users.items()]
        return jsonify(my_users)

    my_users = storage.get("User", user_id)
    if my_users is None:
        abort(404)
    else:
        return jsonify(my_users.to_dict())


@app_views.route('/users/<user_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_users(user_id):
    """ Deletes a User obj based on its' id """

    my_user = storage.get("User", user_id)
    if my_user is None:
        abort(404)
    storage.delete(my_user)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def post_users():
    """ Creates a User """
    content = request.get_json()
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    email = content.get("email")
    if email is None:
        return (jsonify({"error": "Missing email"}), 400)
    password = content.get("password")
    if password is None:
        return (jsonify({"error": "Missing password"}), 400)

    new_user = User(**content)
    new_user.save()

    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=["PUT"], strict_slashes=False)
def update_users(user_id):
    """ Updates a User obj & id """
    content = request.get_json()
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    my_user = storage.get("User", user_id)
    if my_user is None:
        abort(404)

    not_allowed = ["id", "email", "created_at", "updated_at"]
    for key, value in content.items():
        if key not in not_allowed:
            setattr(my_user, key, value)

    my_user.save()
    return (jsonify(my_user.to_dict()), 200)
