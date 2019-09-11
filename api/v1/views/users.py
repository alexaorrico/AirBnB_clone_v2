#!/usr/bin/python3
"""Module for User related endpoints"""
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, make_response, abort, request
from models import storage
from models.user import User

model = "User"


@app_views.route("/users", strict_slashes=False,
                 methods=["GET"], defaults={"user_id": None})
@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """GET /user api route"""
    if not user_id:
        list_objs = [v.to_dict() for v in storage.all(model).values()]
        return jsonify(list_objs)

    return get_model(model, user_id)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """DELETE /user api route"""
    return delete_model(model, user_id)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def post_user():
    """POST /user api route"""
    required_data = {"email", "password"}
    return post_model(model, None, None, required_data)


@app_views.route("/users/<user_id>", methods=["PUT"])
def put_user(user_id):
    """PUT /user api route"""
    ignore_data = ["id", "created_at", "updated_at", "email"]
    return put_model(model, user_id, ignore_data)
