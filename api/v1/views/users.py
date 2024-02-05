#!/usr/bin/python3
""" This file contains the views implementation of
users request as blueprint"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
import json


@app_views.route("/users", methods=["GET", "POST"])
@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"])
def users_view(user_id=None):
    """ View function to retrieve user
    objects"""
    if request.method == "GET" and user_id is None:
        user_objects = storage.all(User).values()
        object_returned = [
                    obj.to_dict() for obj in user_objects
                    ]
        return make_response(jsonify(object_returned), 200)
    if request.method == "POST" and user_id is None:
        if not request.is_json:
            abort(400, description="Not a JSON")
        input_data = request.get_json()   # Not always dict.
        if "email" not in input_data:
            abort(400, "Missing email")
        elif "password" not in input_data:
            abort(400, "Missing password")
        else:
            new_user = User(**input_data)
            storage.new(new_user)
            storage.save()
            return make_response(jsonify(new_user.to_dict()), 201)
    if user_id is not None:
        user_object = storage.get(User, user_id)
        if user_object is None:
            abort(404)
        if request.method == "GET":
            return make_response(jsonify(user_object.to_dict()), 200)
        if request.method == "DELETE":
            storage.delete(user_object)
            storage.save()
            return make_response(jsonify({}), 200)
        if request.method == "PUT":
            if not request.is_json:
                abort(400, description="Not a JSON")
            user_update_data = request.get_json()
            user_update = {
                    key: user_update_data[key]
                    for key in user_update_data
                    if key not in [
                        "id",
                        "email",
                        "created_at",
                        "updated_at"
                        ]
                    }
            user_object.update(user_update)
            storage.save()
            return make_response(jsonify(user_object.to_dict()), 200)
