#!/usr/bin/python3
"""users route handler"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


def check(city_id):
    """
        checking if city valid and linked to state in storage
    """
    try:
        checker = storage.get(User, city_id)
        checker.to_dict()
    except Exception:
        abort(404)
    return checker


def get_all(user_id):
    """
       Retrieves the list of all City objects
       from  state
    """
    if user_id is not None:
        user = check(user_id)
        dict_user = user.to_dict()
        return jsonify(dict_user)
    user_all = storage.all(User)
    users_get_all = []
    for x in user_all.values():
        users_get_all.append(x.to_dict())
    return jsonify(users_get_all)


def delete_user(user_id):
    """
        delete user object
    """
    user = check(user_id)
    storage.delete(user)
    storage.save()
    return jsonify({})


def create_user(request):
    """
        Create new user
    """
    request_json = request.get_json()
    if request_json is None:
        abort(400, 'Not a JSON')
    try:
        email_ = request_json['email']
    except Exception:
        abort(400, "Missing email")
    try:
        password = request_json['password']
    except Exception:
        abort(400, "Missing password")
    user = User(email=email_, password=password)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict())


def update_user(user_id, request):
    """
        update new user
    """
    user_check = check(user_id)
    request_json = request.get_json()
    if request_json is None:
        abort(400, 'Not a JSON')
    for x, y in request_json.items():
        if (x not in ('id', 'created_at', 'updated_at', 'email')):
            setattr(user_check, x, y)
    storage.save()
    return jsonify(user_check.to_dict())


@app_views.route('/users', methods=['GET', 'POST', ],
                 defaults={'user_id': None}, strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def users(user_id):
    """
        Handle cities requests
    """
    if (request.method == "GET"):
        print("hello")
        return get_all(user_id)
    elif (request.method == "DELETE"):
        return delete_user(user_id)
    elif (request.method == "POST"):
        return create_user(request), 201
    elif (request.method == "PUT"):
        return update_user(user_id, request), 200
