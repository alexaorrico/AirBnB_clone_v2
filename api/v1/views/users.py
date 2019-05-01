#!/usr/bin/python3
"""HolbertonBnB User view."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"])
def users():
    """Defines the GET and POST method for users route.

    GET - Retries a list of all the User objects.
    POST - Create a User.
    """

    # GET method
    if request.method == "GET":
        return jsonify([s.to_dict() for s in storage.all("User").values()])

    # POST method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if data.get("name") is None:
        return "Missing name", 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def user_id(user_id):
    """Defines the GET, PUT and DELETE methods for a spacific ID on users.

    GET - Retrieves a User object with the given id.
    PUT - Updates a User object with the given id using a json key/value
    DELETE = Deletes a User object with the given id.
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
        return "Not a JSON", 404
    avoid = {"id", "created_at", "updated_at"}
    [setattr(user, k, v) for k, v in data.items() if k not in avoid]
    user.save()
    return jsonify(user.to_dict())
