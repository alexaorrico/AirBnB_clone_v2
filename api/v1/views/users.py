#!/usr/bin/python3
'''
Create a new view for User object that
handles all default RESTFul API actions
'''

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    '''Retrieve list of all Users'''
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    '''Retrieves User Object'''
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''Deletes User Object'''
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''Creates User Object'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    jsonData = request.get_json()
    if 'email' not in jsonData:
        abort(400, 'Missing email')
    if 'password' not in jsonData:
        abort(400, 'Missing password')
    
    user = User(**jsonData)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    '''Updates User Object'''
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            abort(400, 'Not a JSON')
        jsonData = request.get_json()
        ignoreKeys = ['id', 'email', 'created_at', 'update_at']
        for key, value in jsonData.items():
            if key not in ignoreKeys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    '''404 Not Found'''
    res = {'error': 'Not found'}
    return jsonify(res), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''Bad Request'''
    res = {'error': 'Bad Request'}
    return jsonify(res), 400
