#!/usr/bin/python3
"""
Handles all default RESTful API actions for User objects
"""

from . import app_views
from models import storage
from models.user import User
from flask import abort, jsonify, make_response, request

USER_IGNORE_KEYS = {'id', 'email', 'created_at', 'updated_at'}


@app_views.route("/users", methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    return jsonify([u.to_dict() for u in storage.all('User').values()])


@app_views.route("/users/<user_id>", methods=['GET'])
def get_user(user_id):
    """Retrieves a user given its ID"""
    try:
        return jsonify(storage.get('User', user_id).to_dict())
    except AttributeError:
        abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'])
def del_user(user_id):
    """Deletes a user given its ID"""
    try:
        storage.get('User', user_id).delete()
        return make_response(jsonify({}), 200)
    except AttributeError:
        abort(404)


@app_views.route("/users", methods=['POST'])
def post_user():
    """Creates a user"""
    try:
        r = request.get_json()
        if 'email' not in r:
            abort(make_response(jsonify("Missing name"), 400))
        if 'password' not in r:
            abort(make_response(jsonify("Missing password"), 400))
        u = User(**r)
        u.save()
        return make_response(jsonify(u.to_dict()), 201)
    except TypeError:
        abort(make_response(jsonify("Not a JSON"), 400))


@app_views.route("/users/<user_id>", methods=['PUT'])
def put_user(user_id):
    """Updates a User at a given ID"""
    try:
        u = storage.get('User', user_id)
        if u is None:
            abort(404)
        r = request.get_json()
        for key, value in r.items():
            if key not in USER_IGNORE_KEYS:
                setattr(u, key, value)
    except AttributeError:
        abort(make_response(jsonify("Not a JSON"), 400))
    u.save()
    return make_response(jsonify(u.to_dict()), 200)
