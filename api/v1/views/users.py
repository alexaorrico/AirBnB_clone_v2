#!/usr/bin/python3
"""A Script that handles RESTFul API Actions on user"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, CNC


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """A route that fetches list of all users or create
    a new user.
    Return:
        for GET: list of users in json format
        for POST: Created user with 200 status code
    """
    users = storage.all("User")

    if request.method == 'GET':
        return jsonify(users.to_json())

    if request.method == 'POST':
        request_json = request.get_json()
        if request_json is None:
            abort(400, 'Not a JSON')
        if request_json.get("email") is None:
            abort(400, 'Missing email')
        if request_json.get("password") is None:
            abort(400, 'Missing password')
        new_user = User(**request_json)
        new_user.save()
        return jsonify(new_user.to_json()), 201


@app_views('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def users_by_id(user_id):
    """A route that handles GET, DELETE and PUT request
    based on the user_id.
    Parameters:
        user_id: string(uuid), user id
    Return:
        for GET: user object in json
        for DELETE: empty json
        for PUT: updated user with status code
    """
    user = storage.get("User", user_id)

    if user is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(user.to_json())

    if request.method == 'DELETE':
        user.delete()
        del user
        return jsonify({})

    if request.method == 'PUT':
        request_json = request.get_json()
        if request_json is None:
            abort(400, 'Not a JSON')
        user = bm_update(request_json)
        return jsonify(user.to_json()), 200
