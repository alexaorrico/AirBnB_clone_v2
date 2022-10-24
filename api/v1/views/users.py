#!/usr/bin/python3
"""Routings for amenity-related API requests"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """ get all instance of User """
    if request.method == 'GET':
        return jsonify([v.to_dict() for v in storage.all(User).values()])


@app_views.route('/users/<string:id>', methods=['GET'],
                 strict_slashes=False)
def get_single_user(id):
    """"get an instance of User """
    user = storage.get(User, id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('users/<string:id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(id):
    """ delete an instance of User """
    if request.method == 'DELETE':
        user = storage.get(User, id)
        if user is None:
            abort(404)
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('users', methods=['POST'],
                 strict_slashes=False)
def add_user():
    """ create an instance of User """
    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        body = request.get_json()
        if "email" not in body:
            return make_response(jsonify({"error": "Missing email"}), 400)
        if "password" not in body:
            return make_response(jsonify({"error": "Missing password"}), 400)
        new_user = User(**body)
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)



@app_views.route('/users/<string:id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(id):
    """ update an instance of User """
    if request.method == 'PUT':
        user = storage.get(User, id)
        if user is None:
            abort(404)
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        body = request.get_json()
        for key, value in body.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return make_response(jsonify(user.to_dict()), 200)
