#!/usr/bin/python3
'''Contains the users view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def get_users(user_id=None):
    '''Gets the user with the given id or all users.
    '''
    if user_id:
        v_user = storage.get(User, user_id)
        if v_user:
            obj = v_user.to_dict()
            if 'places' in obj:
                del obj['places']
            if 'reviews' in obj:
                del obj['reviews']
            return jsonify(obj)
        raise NotFound()
    all_v_users = storage.all(User).values()
    my_v_users = []
    for v_user in all_v_users:
        obj = v_user.to_dict()
        if 'places' in obj:
            del obj['places']
        if 'reviews' in obj:
            del obj['reviews']
        my_v_users.append(obj)
    return jsonify(my_v_users)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def remove_user(user_id):
    '''Removes a user with the given id.
    '''
    v_user = storage.get(User, user_id)
    if v_user:
        storage.delete(v_user)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route('/users', methods=['POST'])
def add_user():
    '''Adds a new user.
    '''
    v_data = {}
    try:
        v_data = request.get_json()
    except Exception:
        v_data = None
    if type(v_data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'email' not in v_data:
        raise BadRequest(description='Missing email')
    if 'password' not in v_data:
        raise BadRequest(description='Missing password')
    v_user = User(**v_data)
    v_user.save()
    obj = v_user.to_dict()
    if 'places' in obj:
        del obj['places']
    if 'reviews' in obj:
        del obj['reviews']
    return jsonify(obj), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''Updates the user with the given id.
    '''
    xkeys = ('id', 'email', 'created_at', 'updated_at')
    v_user = storage.get(User, user_id)
    if v_user:
        v_data = {}
        try:
            v_data = request.get_json()
        except Exception:
            v_data = None
        if type(v_data) is not dict:
            raise BadRequest(description='Not a JSON')
        for key, value in v_data.items():
            if key not in xkeys:
                setattr(v_user, key, value)
        v_user.save()
        obj = v_user.to_dict()
        if 'places' in obj:
            del obj['places']
        if 'reviews' in obj:
            del obj['reviews']
        return jsonify(obj), 200
    raise NotFound()

