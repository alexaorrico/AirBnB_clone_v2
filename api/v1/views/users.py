#!/usr/bin/python3
""" View for users """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_user_no_id():
    """ Gets an user if no id has been provided """
    c_user = storage.all(User).values()
    return jsonify([c.to_dict() for c in c_user])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_id(user_id=None):
    """ Gets an user when an id is provided """
    c_user = storage.all(User)
    c_key = "User." + user_id
    if c_key not in c_user:
        abort(404)
    return (jsonify(c_user[c_key].to_dict()))


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def new_user():
    """ Creates a new user """
    js_info = request.get_json()
    if request.is_json is False:
        abort(400, 'Not a JSON')
    if 'email' not in js_info:
        abort(400, 'Missing email')
    if 'password' not in js_info:
        abort(400, 'Missing password')
    new_c = User(**js_info)
    new_c.save()
    return jsonify(new_c.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """ Deletes an user based on the user id """
    c_user = storage.all(User)
    c_key = "User." + user_id
    if c_key not in c_user:
        abort(404)
    storage.delete(c_user[c_key])
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id=None):
    """ Updates an user based on the user id """
    js_info = request.get_json()
    c_user = storage.all(User)
    if request.is_json is False:
        abort(400, 'Not a JSON')
    js_info.pop('id', 'no_error_pls')
    js_info.pop('created_at', 'no_error_pls')
    js_info.pop('updated_at', 'no_error_pls')
    js_info.pop('email', 'no_error_pls')
    c_key = "User." + user_id
    if c_key not in c_user:
        abort(404)
    for key, val in js_info.items():
        setattr(c_user[c_key], key, val)
    storage.save()
    return jsonify(c_user[c_key].to_dict()), 200
