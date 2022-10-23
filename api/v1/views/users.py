#!/usr/bin/python3
"""This module handles user routes"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET', 'POST'])
def users_route():
    """
    users route handles get, post request to users
    """
    if request.method == 'GET':
        user = list(map(lambda obj: obj.to_dict(),
                        storage.all(User).values()))
        return make_response(jsonify(user), 200)
    elif request.method == 'POST':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        required_info = ['email', 'password']
        for info in required_info:
            if info not in form_data:
                return make_response(
                    jsonify({'error': 'Missing {}'.format(info)}), 400)
        new_user = User(**form_data)
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_route(user_id):
    """
    user_route handles get, put, delete requests to a specific
    user

    :param user_id: is the id of the user
    """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    if request.method == 'GET':
        return make_response(jsonify(user.to_dict()), 200)
    elif request.method == 'DELETE':
        user.delete()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        user.update(**form_data)
        return make_response(jsonify(user.to_dict()), 200)
