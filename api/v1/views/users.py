#!/usr/bin/python3
"""api users"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET', 'POST'], strict_slashes=False)
def users():
    '''this function ger all users in the storage,
        if method is get and adds a a user to the datatbase if the method
        is post
    '''
    if request.method == 'GET':
        user_objs = storage.all('User')
        return jsonify([obj.to_dict() for obj in user_objs.values()])

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if data.get("email") is None:
        abort(400, "Missing email")
    if data.get("password") is None:
        abort(400, "Missing password")
    user_obj = User(**data)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<user_id>/', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def get_user(user_id):
    '''
    get or delete or update a user with matching id
    user_id : (string) an id of the user to be worked of accorfing to the
                http method passed
    '''
    user_objs = storage.all('User')
    key = f'User.{user_id}'

    if request.method == 'GET':
        if key in user_objs:
            user = user_objs.get(key)
            return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        if key in user_objs:
            obj = user_objs.get(key)
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    else:
        if key not in user_objs:
            abort(404)
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        user = user_objs.get(key)
        for k, v in data.items():
            setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict()), 200
    abort(404)
