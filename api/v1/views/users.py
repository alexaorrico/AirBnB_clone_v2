#!/usr/bin/python3
""" Createa  new view for State objects that handle restfulapi"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_all_users():
    """ Retrieves list of all Users """
    data = storage.all('User')
    users = [v.to_dict() for k, v in data.items()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_specific_user(user_id):
    """ Retrieves a user object, if not linked, then 404"""
    data = storage.all('User')
    name = 'User.' + user_id
    users = [v.to_dict() for k, v in data.items() if k == name]
    if len(users) != 1:
        abort(404)
    return jsonify(users[0])


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_specific_user(user_id):
    """ Deletes a user object, if not linked, then raise 404 error """
    users = storage.get('User', user_id)
    if not users:
        abort(404)
    storage.delete(users)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a state object """
    new_user_dict = request.get_json(silent=True)
    if new_user_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.json:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**new_user_dict)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates user instance """
    update_user_json = request.get_json(silent=True)
    if update_user_json is None:
        return jsonify({'error': 'Not a JSON'}), 400
    users = storage.all('User')
    user = None
    for u in users:
        if user_id in u:
            user = users[u]
    if not user:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at']
    for k, v in update_state_json.items():
        if k not in ignore:
            setattr(user, k, v)
            storage.save()
    return jsonify(user.to_dict()), 200
