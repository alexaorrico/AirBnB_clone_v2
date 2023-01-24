#!/usr/bin/python3
""" Endpoints for user related
    interactions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def users():
    """retrieve all user objects and
       create new user objects
    """
    if request.method == 'GET':
        all_users = list(storage.all(User).values())
        all_users = [user.to_dict() for user in all_users]
        return jsonify(all_users)

    if request.method == 'POST':
        data = get_json(request)
        if not data:
            return make_response('Not a JSON\n', 400)
        if 'email' not in data.keys():
            return make_response('Missing email\n', 400)
        if 'password' not in data.keys():
            return make_response('Missing password\n', 400)
        new_user = User(**data)
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def user_by_id(user_id):
    """search for a user with given id and:
        1. return their details
        2. update their details
        3. deletes the user
       depending on the method
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = get_json(request)
        if not data:
            return make_response('Not a JSON\n', 400)
        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return make_response(jsonify(user.to_dict()), 200)


def get_json(request):
    """check if body has json data
       and handles errors reponses
    """
    #  exception handling to avoid calling
    #  on_json_loading_failed()
    try:
        data = request.get_json()
    except Exception:
        data = None
    return data
