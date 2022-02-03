#!/usr/bin/python3
'''Contains the users view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.user import User


ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
'''Methods allowed for the users endpoint.'''


@app_views.route('/users', methods=ALLOWED_METHODS)
@app_views.route('/users/<user_id>', methods=ALLOWED_METHODS)
def handle_users(user_id=None):
    '''The method handler for the users endpoint.
    '''
    handlers = {
        'GET': get_users,
        'DELETE': remove_user,
        'POST': add_user,
        'PUT': update_user,
    }
    if request.method in handlers:
        return handlers[request.method](user_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_users(user_id=None):
    '''Gets the user with the given id or all users.
    '''
    all_users = storage.all(User).values()
    if user_id:
        res = list(filter(lambda x: x.id == user_id, all_users))
        if res:
            return jsonify(res[0].to_dict())
        raise NotFound()
    all_users = list(map(lambda x: x.to_dict(), all_users))
    return jsonify(all_users)


def remove_user(user_id=None):
    '''Removes a user with the given id.
    '''
    all_users = storage.all(User).values()
    res = list(filter(lambda x: x.id == user_id, all_users))
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_user(user_id=None):
    '''Adds a new user.
    '''
    data = request.get_json()
    if data is None or type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'email' not in data:
        raise BadRequest(description='Missing email')
    if 'password' not in data:
        raise BadRequest(description='Missing password')
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


def update_user(user_id=None):
    '''Updates the user with the given id.
    '''
    xkeys = ('id', 'created_at', 'updated_at')
    all_users = storage.all(User).values()
    res = list(filter(lambda x: x.id == user_id, all_users))
    if res:
        data = request.get_json()
        if data is None or type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_user = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(old_user, key, value)
        old_user.save()
        return jsonify(old_user.to_dict()), 200
    raise NotFound()
