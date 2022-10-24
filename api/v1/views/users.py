#!/usr/bin/python3
""" New view for users object that handles all
default RESTFul API actions. """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def handle_users():
    """ Retrieves the list of all User objects.
    Creates a new user.
    """
    if request.method == 'GET':
        all_users = storage.all(User).values()
        list_users = [user.to_dict() for user in all_users]
        return jsonify(list_users)

    if request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            abort(400, description="Not a JSON")

        if "email" not in req_data:
            abort(400, description="Missing email")

        if "password" not in req_data:
            abort(400, description="Missing password")

        user = User(**req_data)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_user_id(user_id):
    """ Retrieves, updates or deletes a User object given its id.
    Returns 404 error if id is not found.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        req_data = request.get_json()
        if not req_data:
            abort(400, description='Not a JSON')

        ignore_keys = ['id', 'email', 'created_at', 'updated_at']

        for key, value in req_data.items():
            if key not in ignore_keys:
                setattr(user, key, value)

        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
