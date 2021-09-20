#!/usr/bin/python3
"""module for users view"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response

@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<string:user_id>", strict_slashes=False, methods=["GET"])
def get_users(user_id=None):
    """retrives users"""
    if (not user_id):
        result = []
        for usr in storage.all(User).values():
            result.append(usr.to_dict())
        return jsonify(result)
    else:
        required_user = storage.get(User, user_id)
        if (not required_user):
            abort(404)
        return jsonify(required_user.to_dict())


@app_views.route("/users/<string:user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user(user_id):
    """deletes a user"""
    required_user = storage.get(User, user_id)
    if (not required_user):
        abort(404)
    storage.delete(required_user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """creates a new user"""
    if not request.json:
        return make_response("Not a JSON", 400)
    if not 'email' in request.json:
        return make_response("Missing email", 400)
    if not 'password' in request.json:
        return make_response("Missing password", 400)

    new_user = User(**(request.get_json()))
    new_user.save()
    return new_user.to_dict(), 201


@app_views.route("/users/<string:user_id>", strict_slashes=False, methods=["PUT"])
def edit_user(user_id):
    """edits a user"""
    required_user = storage.get(User, user_id)
    if (not required_user):
        abort(404)
    if not request.json:
        return make_response("Not a JSON", 400)

    input_dict = request.get_json()
    for key, value in input_dict.items():
        if (key not in ["id", "created_at", "updated_at"]):
            if (hasattr(required_user, key)):
                setattr(required_user, key, value)
    required_user.save()
    return required_user.to_dict(), 200
