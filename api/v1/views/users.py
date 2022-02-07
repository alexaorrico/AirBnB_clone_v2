#!/usr/bin/python3
'''Contains the users view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
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
    if user_id:
        user = storage.get(User, user_id)
        if user:
            obj = user.to_dict()
            if 'places' in obj:
                del obj['places']
            if 'reviews' in obj:
                del obj['reviews']
            return jsonify(obj)
        raise NotFound()
    all_users = storage.all(User).values()
    users = []
    for user in all_users:
        obj = user.to_dict()
        if 'places' in obj:
            del obj['places']
        if 'reviews' in obj:
            del obj['reviews']
        users.append(obj)
    return jsonify(users)


def remove_user(user_id=None):
    '''Removes a user with the given id.
    '''
    if user_id:
        user = storage.get(User, user_id)
        if user:
            places = storage.all(Place).values()
            reviews = storage.all(Review).values()
            for place in places:
                if place.user_id == user_id:
                    storage.delete(place)
            for review in reviews:
                if review.user_id == user_id:
                    storage.delete(review)
            storage.delete(user)
            storage.save()
            return jsonify({}), 200
    raise NotFound()


def add_user(user_id=None):
    '''Adds a new user.
    '''
    data = {}
    try:
        data = request.get_json()
    except Exception:
        data = None
    if data is None or type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'email' not in data:
        raise BadRequest(description='Missing email')
    if 'password' not in data:
        raise BadRequest(description='Missing password')
    new_user = User(**data)
    new_user.save()
    obj = new_user.to_dict()
    if 'places' in obj:
        del obj['places']
    if 'reviews' in obj:
        del obj['reviews']
    return jsonify(obj), 201


def update_user(user_id=None):
    '''Updates the user with the given id.
    '''
    xkeys = ('id', 'email', 'created_at', 'updated_at')
    if user_id:
        user = storage.get(User, user_id)
        if user:
            data = {}
            try:
                data = request.get_json()
            except Exception:
                data = None
            if data is None or type(data) is not dict:
                raise BadRequest(description='Not a JSON')
            for key, value in data.items():
                if key not in xkeys:
                    setattr(user, key, value)
            user.save()
            obj = user.to_dict()
            if 'places' in obj:
                del obj['places']
            if 'reviews' in obj:
                del obj['reviews']
            return jsonify(obj), 200
    raise NotFound()
