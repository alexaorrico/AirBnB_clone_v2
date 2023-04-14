#!/usr/bin/python3
""" This module is for user calls to api"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from model.user import User


@app_views.routes(
    "/users",
    strict_slashes=False,
    methos=['GET']
     )
def get_all_users(user_id):
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
    "/users",
    strict_slashes=False,
    methods=["PUTS"]
    )
def puts_usr(user_id):
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
