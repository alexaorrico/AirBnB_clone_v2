#!/usr/bin/python3
"""View for City objects that handles all default RestFul API"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_all_users():
    """Retrieves the list of all User objects"""
    list_users = storage.all(User).values()
    new_list = []
    for value in list_users:
        new_list.append(value.to_dict())
    return (jsonify(new_list))


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """Retrieves User object"""
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    return (jsonify(user_obj.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete users by id"""
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    else:
        user_obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)
