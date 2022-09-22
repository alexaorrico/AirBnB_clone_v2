#!/usr/bin/python3
"""
flask application module for retrieval of
User Objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.exceptions import *
from models.user import User


@app_views.route('/users',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    return (jsonify(User.api_get_all()), 200)


@app_views.route('/users',
                 methods=['POST'],
                 strict_slashes=False)
def post_users():
    """Creates a User"""
    try:
        return (jsonify(
            User.api_post(
                request.get_json(silent=True))),
                201)
    except BaseModelMissingAttribute as attr:
        return (jsonify({'error': 'Missing {}'.format(attr)}), 400)
    except BaseModelInvalidDataDictionary:
        return (jsonify({'error': "Not a JSON"}), 400)


@app_views.route('/users/<string:user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """handles get User object: user_id"""
    try:
        return (jsonify(
            User.api_get_single(user_id)), 200)
    except BaseModelInvalidObject:
        abort(404)


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """handles User object: user_id"""
    try:
        return (jsonify(
            User.api_delete(user_id)), 200)
    except BaseModelInvalidObject:
        abort(404)


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_user_by_id(user_id):
    """handles update of User object: user_id"""
    try:
        return (User.api_put(
                request.get_json(silent=True),
                user_id), 200)
    except BaseModelInvalidDataDictionary:
        return (jsonify({'error': "Not a JSON"}), 400)
    except BaseModelInvalidObject:
        abort(404)
