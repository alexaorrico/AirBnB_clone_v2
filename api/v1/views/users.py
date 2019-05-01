#!/usr/bin/python3
"""Routing for AirBnB user object"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """'GET' response"""
    dic = storage.all(User)
    if request.method == 'GET':
        if user_id is None:
            users_list = []
            for key, value in dic.items():
                users_list.append(value.to_dict())
            return jsonify(users_list)
        else:
            for key, value in dic.items():
                if value.id == user_id:
                    return jsonify(value.to_dict())
            abort(404)


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_user(user_id=None):
    """'DELETE' response"""
    dic = storage.all(User)
    if request.method == 'DELETE':
        empty = {}
        if user_id is None:
            abort(404)
        for key, value in dic.items():
            if value.id == user_id:
                storage.delete(value)
                storage.save()
                return jsonify(empty), 200
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """'POST' response"""
    dic = storage.all(User)
    flag = 0
    if not request.json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    for key in body:
        if key == 'name':
            flag = 1
    if flag == 0:
        abort(400, "Missing name")
    new_user = User(**body)
    storage.new(new_user)
    storage.save()
    new_user_dic = new_user.to_dict()
    return jsonify(new_user_dic), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id=None):
    """'PUT' response"""
    dic = storage.all(User)
    if not request.json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    for key, value in dic.items():
        if value.id == user_id:
            for k, v in body.items():
                setattr(value, k, v)
            storage.save()
            return jsonify(value.to_dict()), 200
    abort(404)
