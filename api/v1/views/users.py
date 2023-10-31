#!/usr/bin/python3
<<<<<<< HEAD
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

=======
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
>>>>>>> 5cec450237a0478b5ae5ad06db65d963f857233f
