#!/usr/bin/python3
"""HolbertonBnB User view."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger import swag_from
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"])
@swag_from("../apidocs/users/get_users.yml", methods=["GET"])
@swag_from("../apidocs/users/post.yml", methods=["POST"])
def users():
    """Defines GET and POST methods for the /users route.

    GET - Retrievs a list of all User objects.
    POST - Creates a User.
    """
    # GET method
    if request.method == "GET":
        return jsonify([u.to_dict() for u in storage.all("User").values()])

    # POST method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if data.get("email") is None:
        return "Missing email", 400
    if data.get("password") is None:
        return "Missing password", 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"])
@swag_from("../apidocs/users/get_user_id.yml", methods=["GET"])
@swag_from("../apidocs/users/delete.yml", methods=["DELETE"])
@swag_from("../apidocs/users/put.yml", methods=["PUT"])
def user_id(user_id):
    """Defines GET, PUT and DELETE methods for a specific ID on /users.

    GET - Retrieves a User object with the given id.
    PUT - Updates a User object with the given id using JSON key/values.
    DELETE - Deletes a User object with the given id.
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    # GET method
    if request.method == "GET":
        return jsonify(user.to_dict())

    # DELETE method
    elif request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({})

    # PUT method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    avoid = {"id", "email", "created_at", "updated_at"}
    [setattr(user, k, v) for k, v in data.items() if k not in avoid]
    user.save()
    return jsonify(user.to_dict())
