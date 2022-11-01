#!/usr/bin/python3
"""
a view for User object that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET', 'POST'])
def get_add_users():
    """
    get user information for all users
    """
    userObjs = storage.all("User")
    if request.method == 'GET':
        users = []
        for user in userObjs.values():
            users.append(user.to_dict())
        return jsonify(users)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'email' not in request.get_json():
            return make_response(jsonify({'error': 'Missing email'}), 400)
        if 'password' not in request.get_json():
            return make_response(jsonify({'error': 'Missing password'}), 400)
        kwargs = request.get_json()
        user = User(**kwargs)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['GET', 'DELETE', 'PUT'])
def Manageusers(user_id):
    """
    manipulate city information for specified city
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return (jsonify({}))

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in request.get_json().items():
            if attr not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, attr, val)
        user.save()
        return jsonify(user.to_dict())
