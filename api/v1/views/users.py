#!/usr/bin/python3
""" Handles all default RESTFul API actions for User object """
import re
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getUsers():
    """ Return all users in a JSON format """
    users = []
    all_u = storage.all('User').values() 
    for user in all_u:
        users.append(all_u.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_iD(user_id=None):
    """ Retrieves a user with his iD """
    users = storage.all('User', user_id).values() 
    if users: 
        return jsonify(users.to_dict())
    abort(404)

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """ Delete a user"""
    if user_id:
        user = storage.get("User", user_id)
        if user:
            storage.delete(user)
            storage.save()
            return jsonify({}), 200
    abort(404)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates user """
    user_dict = request.get_json()
    if not user_dict:
        abort (400, "Not a JSON")
    elif 'email' not in user_dict.keys():
        abort (400, "Missing email")
    elif 'password' not in user_dict.keys():
        abort (400, "Missing password")
    new_u = User(**user_dict)
    new_u.save()
    return (jsonify(new_u.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_review(user_id):
    """update a user"""
    user = storage.get("User", user_id)
    if user:
        req = request.get_json()
        if req is None:
            abort(400, "Not a JSON")
        for key, value in req.items():
            setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    abort(404)
