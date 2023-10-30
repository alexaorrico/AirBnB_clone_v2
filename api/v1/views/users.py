#!/usr/bin/python3
"""Module containing a Flask Blueprint routes that handles
all default RESTFul API actions for User resource"""
from api.v1.views import app_views
from flask import abort, make_response, jsonify, request
from hashlib import md5
from markupsafe import escape
from models import storage
from models.user import User


def retrive_object(cls, id):
    """Retrive a resource based on given class and id."""
    obj = storage.get(cls, escape(id))
    if obj is None:
        abort(404)
    return (obj)


def validate_request_json(request):
    """Checks validity of request's json content"""
    if not request.is_json:
        abort(make_response(jsonify(error="Not a JSON"), 400))
    req_json = request.get_json()
    if request.method == 'POST':
        if 'email' not in req_json:
            abort(make_response(jsonify(error="Missing email"), 400))
        if 'password' not in req_json:
            abort(make_response(jsonify(error="Missing password"), 400))
    return (req_json)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def users_get(user_id=None):
    """Returns a User with given id, or all users if no id is given"""
    if user_id is None:
        users = storage.all(User).values()
        return (jsonify([user.to_dict() for user in users]))
    user = retrive_object(User, user_id)
    return (jsonify(user.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def users_delete(user_id):
    """Deletes a User resource based on given id"""
    user = retrive_object(User, user_id)
    storage.delete(user)
    storage.save()
    return (jsonify({}))


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users_post():
    """Creates a User resource if request content is valid."""
    req_json = validate_request_json(request)
    new_user = User(**req_json)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def users_put(user_id):
    """Updates a User resource of given id if request content is valid."""
    user = retrive_object(User, user_id)
    req_json = validate_request_json(request)
    ignore = ['id', 'email', 'created_at', 'password', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore:
            setattr(user, key, value)
        if key == 'password':  # hash password
            setattr(user, key, md5(value.encode()).hexdigest())
    user.save()
    return (jsonify(user.to_dict()))
