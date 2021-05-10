#!/usr/bin/python3
"""index file"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

from flask import request


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """All users"""
    states_dict = []
    for item in storage.all('User').values():
        states_dict.append(item.to_dict())
    return jsonify(states_dict)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """User"""
    if storage.get('User', user_id) is None:
        abort(404)
    else:
        return jsonify(storage.get('User', user_id).to_dict())


@app_views.route("/users/<user_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id=None):
    """state"""
    willy = storage.get('User', user_id)
    if willy is None:
        abort(404)
    else:
        storage.delete(willy)
        storage.save()
        return jsonify({}), 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def post_user(state_id=None):
    """state"""
    try:
        willy = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if willy is None:
        abort(400, 'Not a JSON')
    elif "email" not in willy.keys():
        abort(400, 'Missing email')
    elif "password" not in willy.keys():
        abort(400, 'Missing password')
    else:
        new_user = User(name=willy['name'])
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def put_user(state_id=None):
    """put/update state"""
    """ Request dict """
    user_store = storage.get(User, user_id)
    try:
        dict_w = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if state_id is None:
        abort(404)
    if dict_w is None:
        abort(400, 'Not a JSON')
    for key, val in dict_w.items():
        if key == 'id' or key == 'email' or key == 'updated_at' or\
           key == 'created_at':
            pass
        else:
            if user_store is not None:
                setattr(user_store, key, val)
                user_store.save()
                return jsonify(user_store.to_dict()), 200
    abort(404)
