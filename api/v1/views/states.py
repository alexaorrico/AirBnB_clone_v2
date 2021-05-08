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


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """states"""
    states_dict = []
    for item in storage.all('State').values():
        states_dict.append(item.to_dict())
    return jsonify(states_dict)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """state"""
    if storage.get('State', state_id) is None:
        abort(404)
    else:
        return jsonify(storage.get('State', state_id).to_dict())


@app_views.route("/states/<state_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id=None):
    """state"""
    willy = storage.get('State', state_id)
    if willy is None:
        abort(404)
    else:
        storage.delete(willy)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state(state_id=None):
    """state"""
    try:
        willy = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if willy is none:
        abort(400, 'Not a JSON')
    elif "name" not in willy.keys():
        abort(400, 'Missing name')
    else:
        new_state = State(name=willy['name'])
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def put_state(state_id=None):
    """put/update state"""
    """ Request dict """
    state_store = storage.get(State, state_id)
    try:
        dict_w = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if state_id is None:
        abort(404)
    if dict_w is None:
        abort(400, 'Not a JSON')
    for key, val in dict_w.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(state_store, key, val)
    state_store.save()
    return jsonify(state_store.to_dict()), 200
