#!/usr/bin/python3
""" users routes """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def users():
    """ list of users """
    users = storage.all('User')
    return jsonify([value.to_dict() for value in users.values()])


@app_views.route('/users/<string:id>', strict_slashes=False)
def user_id(id):
    """ json data of a single user """
    single_user = storage.get('User', id)
    if single_user:
        return jsonify(single_user.to_dict()), 200
    abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def insert_user():
    """ Creates a new user """
    dictionary = request.get_json()
    if dictionary is None:
        abort(400, 'Not a JSON')
    if dictionary.get('email') is None:
        abort(400, 'Missing email')
    if dictionary.get('password') is None:
        abort(400, 'Missing password')
    user = User(**dictionary)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:id>', strict_slashes=False, methods=['PUT'])
def update_user(id):
    """ Updates one user """
    dictionary = request.get_json()
    if dictionary is None:
        abort(400, 'Not a Json')
    single_user = storage.get('User', id)
    if single_user is None:
        abort(404)
    [setattr(single_user, key, value) for key, value in dictionary.items()
        if key not in ['id', 'created_at', 'updated_at', 'email']]
    single_user.save()
    return jsonify(single_user.to_dict())


@app_views.route('/users/<string:id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(id):
    """ Deletes one user """
    single_user = storage.get('User', id)
    if single_user is None:
        abort(404, 'Not found')
    single_user.delete()
    storage.save()
    return jsonify({})
