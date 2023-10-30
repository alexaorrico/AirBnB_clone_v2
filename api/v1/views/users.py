#!/usr/bin/python3
"""users al7bin"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User
from json import dumps


def json_ser(obj):
    json_obj = {}
    for key in obj:
        json_obj[key] = obj[key].to_dict()
    return (json_obj)


def cities_json(lst):
    json_list = []
    for city in lst:
        json_list.append(city.to_dict())
    return (json_list)


@app_views.route('/users', methods=['GET'])
def get_users():
    return make_response(
        dumps(list(json_ser(storage.all(User)).values())),
        200)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    return (user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(({}), 200)


@app_views.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")
    user = User(**data)
    storage.new(user)
    storage.save()
    return make_response((user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key in data:
        if key in ['id', 'email', 'created_at', 'updated_at']:
            continue
        value = data[key]
        if hasattr(user, key):
            try:
                value = type(getattr(user, key))(value)
            except ValueError:
                pass
            setattr(user, key, value)
    storage.save()
    return make_response(user.to_dict(), 200)
