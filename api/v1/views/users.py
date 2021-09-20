#!/usr/bin/python3
"""
script that starts a Flask web application:
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def user_all():
    """
    Retrieves a User object:
    """
    list = []
    for user in storage.all("User").values():
        list.append(user.to_dict())
    return jsonify(list)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def us_all(user_id):
    """
    Retrieves a amenity object:
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def user_delete(user_id):
    """
    Deletes a User object
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """
    Creates a User
    """
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json().keys():
        abort(400, "Missing email")
    if "password" not in request.get_json().keys():
        abort(400, "Missing password")
    else:
        my_user = User(**request.get_json())
        storage.new(my_user)
        storage.save()
        resp = my_user.to_dict()
        return jsonify(resp), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    """
    Updates a User object
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    us = request.get_json()
    if us is None:
        abort(400, "Not a JSON")
    else:
        for key, value in us.items():
            if key in ['id'] and key in ['created_at']\
                    and key in ['email'] and key in ['updated_at']:
                pass
            else:
                setattr(user, key, value)
        storage.save()
        resp = user.to_dict()
        return jsonify(resp), 200
