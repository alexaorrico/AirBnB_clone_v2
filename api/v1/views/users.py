#!/usr/bin/python3
""" Create a new view for User objects that handles all
    default RESTFul API actions
"""


from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models.user import User
from models import storage


@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
@app_views.route("/users", methods=['GET'],
                 strict_slashes=False)
def user_abor(user_id=None):
    """ Retrieves the list of all state.cities objects """
    user = storage.all("User")
    lista = []
    if user_id is None:
        for values in user.values():
            lista.append(values.to_dict())
        return jsonify(lista)
    else:
        user_exist = storage.get('User', user_id)
        if user_exist is None:
            abort(404)
        return jsonify(user_exist.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def user_del(user_id=None):
    """ delete a user by id """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """ post method user, You must use request.get_json from Flask """
    json_data = request.get_json()

    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'email' not in json_data:
        return jsonify({'error': 'Missing email'}), 400

    if 'password' not in json_data:
        return jsonify({'error': 'Missing password'}), 400

    user = User(**json_data)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id=None):
    """ method put Updates a User object: PUT """
    p_user = storage.get("User", user_id)
    if p_user is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key != "__class__":
            setattr(p_user, key, value)
    storage.save()
    return jsonify(p_user.to_dict()), 200
