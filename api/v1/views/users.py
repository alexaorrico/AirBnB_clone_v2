#!/usr/bin/python3
"""users route handler"""
from flask import jsonify, abort, request
from api.v1.app import *
from api.v1.views import *
from models import storage, user

def validate(user_id):
    """ validate if query have id to reference """
    try:
        valid = storage.get(User, user_id)
        valid.to_dict()
    except Exception:
        abort(404)
    return valid


def get_all_users(user_id):
    """ get all users """
    if user_id is not None:
        get_user = validate(user_id).to_dict()
        """ dict_user = get_user.to_dict() """
        return jsonify(get_user)
    users = storage.all(User)
    users_all = []
    for user in users.values():
        users_all.append(user.to_dict())
    return jsonify(users_all)


def delete_user(user_id):
    """ delete user """
    user = validate(user_id)
    storage.delete(user)
    storage.save()
    response = {}
    return jsonify(response)


def create_user(request):
    """ create user """
    request_json = request.get_json()
    if request_json is None:
        abort(400, 'Not a JSON')
    try:
        email_usr = request_json['email']
    except Exception:
        abort(400, "Missing email")
    try:
        password = request_json['password']
    except Exception:
        abort(400, "Missing password")
    user = User(email=email_usr, password=password)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict())


def update_user(user_id, request):
    """ update user """
    user = validate(user_id)
    request_json = request.get_json()
    if (request_json is None):
        abort(400, 'Not a JSON')
    for key, value in request_json.items():
        if (key not in ('id', 'created_at', 'updated_at', 'email')):
            setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict())


@app_views.route('/users/', methods=['GET', 'POST', ],
                 defaults={'user_id': None}, strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def users(user_id):
    """ users route """
    if (request.method == "GET"):
        return get_all_users(user_id)
    elif (request.method == "DELETE"):
        return delete_user(user_id)
    elif (request.method == "POST"):
        return create_user(request), 201
    elif (request.method == "PUT"):
        return update_user(user_id, request), 200