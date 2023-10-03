#!/usr/bin/python3
"""script that starts a Flask web application"""


from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User

app = Flask(__name__)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all('User')
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list), 200


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id=None):
    """Retrieves a User object with the id linked to it"""
    users = storage.all('User')
    user = users.get('User' + "." + user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """Deletes a User object"""
    obj = storage.get('User', user_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a User"""
    result = request.get_json()
    if not result:
        abort(400, {"Not a JSON"})
    if 'email' not in result:
        abort(400, {"Missing email"})
    if 'password' not in result:
        abort(400, {"Missing password"})
    obj = User()
    for key, value in result.items():
        setattr(obj, key, value)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id=None):
    """Updates a User object"""
    result = request.get_json()
    if not result:
        abort(400, {"Not a JSON"})
    obj = storage.get('User', user_id)
    if obj is None:
        abort(404)
    invalid_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in result.items():
        if key not in invalid_keys:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
