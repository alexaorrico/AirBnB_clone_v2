#!/usr/bin/python3
"""Create a new view for User objects that
handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ Gets all User objects """
    all_user_list = []
    for value in storage.all(User).values():
        all_user_list.append(value.to_dict())
    return jsonify(all_user_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Gets a User object """
    user_obj = storage.get(User, user_id)
    if user_obj:
        return jsonify(user_obj.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user_obj = storage.get(User, user_id)
    if user_obj:
        storage.delete(user_obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates a new User object """
    json_body = request.get_json()
    if json_body:
        if 'email' not in json_body:
            return make_response(jsonify({'error': 'Missing email'}), 400)
        elif 'password' not in json_body:
            return make_response(jsonify({'error': 'Missing password'}), 400)
        else:
            new_user = User(**json_body)
            new_user.save()
            return make_response(jsonify(new_user.to_dict()), 201)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates a User object"""
    json_body = request.get_json()
    user_obj = storage.get(User, user_id)
    if json_body:
        if user_obj:
            for key, value in json_body.items():
                if key not in ['id', 'email', 'created_at', 'updated_at']:
                    setattr(user_obj, key, value)
            user_obj.save()
            return make_response(jsonify(user_obj.to_dict()), 200)
        else:
            abort(404)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
