#!/usr/bin/python3
""" handles all default RestFul API """
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models.user import User
from models import storage


@app_views.route('/users', methods=["GET"], strict_slashes=False)
def users_view():
    """ return a jsonified user objects """
    users_list = []
    for value in storage.all(User).values():
        users_list.append(value.to_dict())
    return (jsonify(users_list))


@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def users_id_view(user_id):
    """ returns a jsonified user obj by user_id """
    get_id = storage.get(User, user_id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """ delete user obj by user_id """
    get_id = storage.get(User, user_id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
    """ creating a user object """
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    if "email" not in data_req.keys():
        return (make_response(jsonify({'error': 'Missing email'}), 400))
    if "password" not in data_req.keys():
        return (make_response(jsonify({'error': 'Missing password'}), 400))
    new_user_obj = User(**data_req)
    new_user_obj.save()
    return (jsonify(new_user_obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """ updating a user object """
    get_id = storage.get(User, user_id)
    if get_id is None:
        abort(404)
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    for key, value in data_req.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(get_id, key, value)
    get_id.save()
    return (jsonify(get_id.to_dict()), 200)
