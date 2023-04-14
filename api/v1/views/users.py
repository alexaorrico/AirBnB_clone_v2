#!/usr/bin/python3
""" This module is for user calls to api"""

from flask import abort, jsonify, make_response, request
from models.user import User
from models import storage

from api.v1.views import app_views


@app_views.routes(
    "/users",
    strict_slashes=False,
    methods=['GET']
     )
def get_all_users(user_id):
    """
    This module gets all users from the storage and retuns a json
    """
    all_usr = storage.all(User)
    if user_id is None:
        abort(404)
    all_usrs = []
    for usr in all_usr.values():
        all_usrs.append(usr.to_dict())
    return jsonify(all_usrs)


@app_views.routes(
    "/users/<user_id>",
    strict_slashes=False,
    methods=["GET"]
    )
def retrive_user(user_id):
    """
    This module returns a user with the specific user id pass as argument
    """
    usr = storage.get(User, user_id)
    if usr is None:
        abort(404)
    return jsonify(usr.to_dict())


@app_views.routes(
    "/users",
    strict_slashes=False,
    methods=["POST"]
    )
def post_user():
    """
    This module post a new user to the data base
    """
    usr = request.get_json()
    if usr is None:
        abort(400, 'Not a JSON')
    if 'email' is None:
        abort(400, 'Missing email')
    if 'password' is None:
        abort(400, 'Missing password')
    user = User(**usr)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.routes(
    "/users/<user_id>",
    strict_slashes=False,
    methods=["DELETE"]
    )
def delete_usr(user_id):
    """
    This module deletes user from data base
    """
    usr = storage.get(User, user_id)
    if user_id is None:
        abort(404)
    storage.delete(usr)
    storage.save()
    return jsonify({}, 200)


@app_views.routes(
    "/users",
    strict_slashes=False,
    methods=["PUT"]
    )
def put_usr(user_id):
    """ 
    This module updates user info in the data bsae
    """
    if user_id is None:
        abort(404)
    usr = request.get_json()
    if usr is None:
        abort(400, 'Nont a JSON')
    for key, value in usr.item():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(usr, key, value)
    usr.save()
    return make_response(jsonify(usr.to_dict()), 200)
