#!/usr/bin/python3
"""users view module"""
from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """returns list of all users"""
    if request.method == 'GET':
        users_list = []
        for user, value in storage.all(User).items():
            user = value.to_dict()
            users_list.append(user)
        return jsonify(users_list)

    if request.method == 'POST':
        # If not valid JSON, error 400
        try:
            request_data = request.get_json()
            if 'email' not in request_data:
                abort(400, "Missing email")
            if 'password' not in request_data:
                abort(400, "Missing password")
            newuser = user(**request_data)
            newuser.save()
        except Exception:
            abort(400, "Not a JSON")
        return jsonify(newuser.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_search(user_id):
    """returns user with id or 404"""

    #  If GET
    if request.method == 'GET':
        for user, value in storage.all(User).items():
            id = (user.split(".")[1])
            if user_id == id:
                return jsonify(value.to_dict())
        abort(404)

    #  If DELETE
    if request.method == 'DELETE':
        user = storage.get(user, user_id)
        if user is not None:
            storage.delete(user)
            storage.save()
            return jsonify({})
        else:
            abort(404)

    # If PUT
    if request.method == 'PUT':
        # If not valid JSON, error 400
        try:
            request_data = request.get_json()
            for user, value in storage.all(User).items():
                id = (user.split(".")[1])
                if user_id == id:
                    for k in request_data.keys():
                        if k != 'id' and k != 'email' and\
                                k != 'created_at' and k != 'updated_at':
                            setattr(value, k, request_data[k])
                    storage.save()
                return jsonify(value.to_dict())
        except Exception:
            abort(400, "Not a JSON")
        abort(404)