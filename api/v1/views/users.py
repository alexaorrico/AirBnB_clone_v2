#!/usr/bin/python3
"""Renders json view for User object(s)
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/users",
                 strict_slashes=False, methods=['GET'])
def all_users():
    """Returns list of json representation of all users
    """
    users = storage.all("User")
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route("/users/<user_id>",
                 strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """Returns a user
    Raises 404 if no user found based on user_id
    """
    user = storage.get("User", user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route("/users/<user_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """delete an user object from storage
    """
    user = storage.get("User", user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/users/<user_id>",
                 strict_slashes=False, methods=['PUT'])
def modify_user(user_id):
    """modify an user object
    """
    ignore = ["id", "email", "created_at", "updated_at"]
    user = storage.get("User", user_id)
    if user:
        body = request.get_json()
        if not body:
            return make_response('Not a JSON', 400)
        for k, v in body.items():
            if k not in ignore:
                setattr(user, k, v)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
    abort(404)


@app_views.route("/users",
                 strict_slashes=False, methods=['POST'])
def create_user():
    """create a user
    """
    from models.user import User
    body = request.get_json()
    if not body:
        return make_response('Not a JSON', 400)
    if not body.get('email'):
        return make_response('Missing email', 400)
    if not body.get('password'):
        return make_response('Missing password', 400)
    user = User(email=body.get('email'), password=body.get('password'))
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)
