#!/usr/bin/python3
"""
Define User routes.
"""


from flask import request, abort, jsonify
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route("/users", methods=["GET", "POST"])
def users():
    """Define /users route with GET and POST methods
    POST - Create a new user
    GET - Get a list of all users
    """
    # GET
    if request.method == "GET":
        return jsonify(
            [user.to_dict() for user in storage.all('User').values()]
        )

    # POST
    doc = request.get_json(silent=True)
    if doc is None:
        return "Not a JSON", 400
    if doc.get("email") is None:
        return "Missing email", 400
    if doc.get("password") is None:
        return "Missing password", 400
    user = User(**doc)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"])
def user(user_id):
    """Define /users/<user_id> with GET, PUT and DELETE  methods
    GET - get a user with the given id
    PUT - Update the user with the given id
    DELETE - Delete the user with the given id
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    # GET
    if request.method == "GET":
        return jsonify(user.to_dict())

    # PUT
    elif request.method == 'PUT':
        doc = request.get_json(silent=True)
        if doc is None:
            return "Not a JSON", 400

        for k, v in doc.items():
            if k not in ('id', 'email', 'created_at', 'updated_at'):
                if k == 'password':
                    User.hash_password(user, v)
                else:
                    setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict()), 200

    # DELETE
    user.delete()
    storage.save()
    return jsonify({}), 200
