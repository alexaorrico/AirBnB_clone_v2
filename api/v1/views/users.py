#!/usr/bin/python3
""" users RESTfull API handler """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'])
def get_users():
    """ get all users """
    my_list = []
    users = storage.all("User")
    for user in users.values():
        my_list.append(user.to_dict())
    return jsonify(my_list)


@app_views.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    """get user by id"""
    try:
        return jsonify(storage.get("User", user_id).to_dict())
    except:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """delete user by id"""
    try:
        my_user = storage.get("User", user_id)
        my_user.delete()
        return {}, 200
    except:
        abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """creates a new user"""
    try:
        return {}, 200
    except:
        abort(404)
