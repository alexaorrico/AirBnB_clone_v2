#!/usr/bin/python3
""" cities view module """

from api.v1.views import app_views
from flask import make_response
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """ Get all users """
    all = storage.all(User)

    users = []

    for one in all.values():
        users.append(one.to_dict())

    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_a_user(user_id):
    """ Get a user with a given user_id """
    if User.__name__ + '.' + user_id not in storage.all(User).keys():
        abort(404)
    user = storage.get(User, user_id)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """ Delete a user if user exists """
    try:
        storage.all().pop(User.__name__ + '.' + user_id)
        storage.save()
        return jsonify({})
    except KeyError:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """ Create a new user
        email and password is compulsory
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'email' not in data:
        return make_response(jsonify({'error': 'Missing email'}), 400)

    if 'password' not in data:
        return make_response(jsonify({'error': 'Missing password'}), 400)

    user = User(**data)
    user.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def edit_user(user_id):
    """ Edit a user information """
    users = storage.all(User)

    if User.__name__ + '.' + user_id not in users.keys():
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if not data['name']:
        return make_response(jsonify({'error': 'Missing name'}), 404)

    user = User(**data)
    user.save()

    return jsonify(storage.get(User, user.id).to_dict())
