#!/usr/bin/python3
"""
view for User objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def users():
    """ Retrieves the list of all User objects """
    all_users = storage.all(User)
    return jsonify([obj.to_dict() for obj in all_users.values()])


@app_views.route('/users/<user_id>', strict_slashes=False)
def user_id(user_id):
    """ Retrieves a User object """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """ Creates a User """
    newuser = request.get_json()
    if not newuser:
        abort(400, "Not a JSON")
    if "email" not in newuser:
        abort(400, "Missing email")
    if "password" not in newuser:
        abort(400, "Missing password")

    user = User(**newuser)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    """ Updates a User object """
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    for key, value in request_body.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(user, key, value)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
