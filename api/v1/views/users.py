#!/usr/bin/python3
""" User view """
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """ Retrieves the list of all User objects """
    users = storage.all(User)
    return jsonify([obj.to_dict() for obj in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_id(user_id):
    """ Retrieves a User object """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Create a new User """
    new_user = request.get_json()
    if new_user is None:
        abort(400, 'Not a JSON')
    if 'email' not in new_user:
        abort(400, 'Missing email')
    if 'password' not in new_user:
        abort(400, 'Missing password')
    user = User(**new_user)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_id_put(user_id):
    """ Updates a User object """
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    request_json = request.get_json()
    if not request_json:
        abort(400, "Not a JSON")
    for key, value in request_json.items():
        if key != 'id' and key != 'email' and \
                key != 'created_at' and key != 'updated_at':
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
