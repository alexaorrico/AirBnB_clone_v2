#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    """ Return all users """
    catch_users = []
    for user in storage.all('User').values():
        catch_users.append(user.to_dict())
    return jsonify(catch_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """ Return the user form a id """
    catch_user = storage.get('User', user_id)
    if catch_user is None:
        abort(404)
    return jsonify(catch_user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user_id(user_id):
    """ Delete the user form a id """
    catch_user = storage.get('User', user_id)
    if catch_user is None:
        abort(404)
    storage.delete(catch_user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Method to update an user"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user_id(user_id):
    """ Method to update an user with id"""
    catch_user = storage.get('User', user_id)
    if catch_user is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(catch_user, key, value)
    storage.save()
    return jsonify(catch_user.to_dict()), 200
