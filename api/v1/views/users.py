#!/usr/bin/python3
""" Users view """
from flask import jsonify, make_response, request
from api.v1.views import app_views, User
from models import storage
from flask import abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrives all users objects"""
    objects = storage.all(User)
    list_values = []
    for key, value in objects.items():
        list_values.append(value.to_dict())
    return jsonify(list_values)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_users_by_id(user_id):
    """ Get users by ID """
    user_object = storage.get(User, user_id)
    result = None
    if user_object.__class__.__name__ == 'User':
        result = jsonify(user_object.to_dict())
    else:
        result = abort(404)
    return result


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_users(user_id):
    """ DELETE users by ID """
    user_object = storage.get(User, user_id)
    result = None
    if user_object.__class__.__name__ == 'User':
        storage.delete(user_object)
        storage.save()
        result = make_response(jsonify({}), 200)
    else:
        result = abort(404)
    return result


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    """ ADD users """
    if request.is_json:
        data = request.get_json()
        if 'email' not in data:
            result = jsonify({'error': 'Missing email'}), 400
        elif 'password' not in data:
            result = jsonify({'password': 'Missing password'}), 400
        else:
            new_object = User(**data)
            storage.new(new_object)
            storage.save()
            result = jsonify(new_object.to_dict()), 201
    else:
        result = jsonify({'error': 'Not a JSON'}), 400
    return result


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_users(user_id):
    """ PUT users """
    user_object = storage.get(User, user_id)
    if not user_object.__class__.__name__ == 'User':
        return abort(404)
    if request.is_json:
        data = request.get_json()
        for key, value in data.items():
            setattr(user_object, key, value)
        storage.save()
        result = jsonify(user_object.to_dict()), 200
    else:
        result = jsonify({'error': 'Not a JSON'}), 400
    return result
