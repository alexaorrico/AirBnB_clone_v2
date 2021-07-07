#!/usr/bin/python3
"""
module: users
create api routes:
/status: return status always ok, method GET
/stats: return quantity of tables or clases. method GET
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def displayUsers():
    """Return all the users
    """
    list_users = []
    users = storage.all('User')
    for key, value in users.items():
        list_users.append(value.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET\
'], strict_slashes=False)
def displayUserById(user_id):
    """Return user by id
    """
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE\
'], strict_slashes=False)
def deleteUser(user_id):
    """Delete an user if not error 404
    """
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createUser():
    """Create an user if not error 404
    """
    flag = 0
    user = request.get_json()
    if not user:
        abort(400, {'Not a JSON'})
    if 'email' not in user:
        abort(400, {'Missing name'})
    if 'password' not in user:
        abort(400, {'Missing password'})
    new_user = User(**user)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT\
'], strict_slashes=False)
def updateUser(user_id):
    """Update an user if not error 404
    """
    flag = 0
    user = request.get_json()
    text_final = "{}.{}".format('User', user_id)
    if not user:
        abort(400, {'Not a JSON'})
    us = storage.get('User', user_id)
    if not us:
        abort(404)
    ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in user.items():
        if key not in ignore:
            setattr(us, key, value)
    storage.save()
    return jsonify(us.to_dict()), 200
