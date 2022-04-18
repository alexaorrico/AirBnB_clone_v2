#!/usr/bin/python3
""" cities view module """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """ Get all users """
    all = storage.all(User)

    users = []

    for one in all.values():
        users.append(one.to_dict())

    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_a_user(user_id):
    """ Get a user with a given user_id """
    if User.__name__ + '.' + user_id not in storage.all(User).keys():
        abort(404)
    user = storage.get(User, user_id)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Delete a user if user exists """
    try:
        storage.all().pop(User.__name__ + '.' + user_id)
        storage.save()
        return jsonify({}), 200
    except KeyError:
        abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """ Create a new user
        email and password is compulsory
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()
    else:
        abort(400, description='Not a JSON')

    if 'email' not in data:
        abort(400, 'Missing email')

    if 'password' not in data:
        abort(400, 'Missing password')

    user = User(**data)
    user.save()

    return jsonify(storage.get(User, user.id).to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def edit_user(user_id):
    """ Edit a user information """
    users = storage.all(User)

    if User.__name__ + '.' + user_id not in users.keys():
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()
    else:
        abort(400, description='Not a JSON')

    if not data['name']:
        abort(404, description='Missing name')

    user = User(**data)
    user.save()

    return jsonify(storage.get(User, user.id).to_dict()), 200
