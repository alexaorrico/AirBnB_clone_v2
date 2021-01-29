#!/usr/bin/python3
""" new view for Users objects """

from models.user import User
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage, base_model


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    if request.method == 'GET':
        user_list = []
        for ob in storage.all(User).values():
            user_list.append(ob.to_dict())
        return jsonify(user_list), 200


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user_id(user_id):
    """Retrieves a User by id"""
    if request.method == 'GET':
        ob = storage.get(User, user_id)
        if ob is not None:
            return jsonify(ob.to_dict())
        return abort(404)


@app_views.route(
    '/users/<user_id>',
    strict_slashes=False,
    methods=['DELETE']
)
def delete_user_ob(user_id):
    """Delete a User object by id"""
    if request.method == 'DELETE':
        ob = storage.get(User, user_id)
        if ob is not None:
            storage.delete(ob)
            storage.save()
            return jsonify({}), 200
        else:
            return abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user_ob():
    """Create a User object"""
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return "Not a JSON", 400
        elif "email" not in data:
            return "Missing email", 400
        elif "password" not in data:
            return "Missing password", 400
        else:
            ob = User(**data)
            storage.new(ob)
            storage.save()
            return jsonify(ob.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user_ob(user_id):
    """Update a User object"""
    if request.method == 'PUT':
        ob = storage.get(User, user_id)
        data = request.get_json()
        if not ob:
            return abort(404)
        if not data:
            return "Not a JSON", 400
        for key, val in data.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(ob, key, val)
        storage.save()
        return jsonify(ob.to_dict()), 200
