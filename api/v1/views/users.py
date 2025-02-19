#!/usr/bin/python3
""" script for State view """

from models import storage
from models.user import User
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort
from flask import request, make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_user():
    """Route that returns all user"""
    all_list = []
    user_dict = storage.all(User)
    for _, obj in user_dict.items():
        all_list.append(obj.to_dict())

    return make_response(jsonify(all_list), 200)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """Route that returns a user by its ID"""
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)

    return make_response(jsonify(user_obj.to_dict()), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def user_delete(user_id):
    """ delete http request"""
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """post http request """
    if not request.json:
        abort(400, description="Not a JSON")
    if 'email' not in request.json:
        abort(400, description="Missing email")
    if 'password' not in request.json:
        abort(400, description="Missing password")

    request_dict = request.get_json()
    obj = User()

    for k, v in request_dict.items():
        setattr(obj, k, v)

    # add obj to current DB session and save it.
    storage.new(obj)
    storage.save()
    new_state = obj.to_dict()
    return make_response(jsonify(new_state), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def user_update(user_id):
    """put http request"""
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    new_dict = request.get_json()
    ignore_keys = {'id', 'email', 'created_at', 'updated_at'}
    for k, v in new_dict.items():
        if k not in ignore_keys:
            setattr(user_obj, k, v)

    storage.save()
    return make_response(jsonify(user_obj.to_dict()), 200)
