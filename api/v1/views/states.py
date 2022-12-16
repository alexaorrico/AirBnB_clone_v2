#!/usr/bin/python3
""" new view for State objects """

from models import storage
from api.v1.views import app_views
from models.state import State
from flask import Flask, make_response, jsonify
import requests
from flask import request


""" Method GET """
@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>')
def get_states(state_id=None):
    """ Retrieves the list of all State objects """
    if state_id is None:
        state_objs = [state.to_dict() for state in storage.all(State).values()]
        return make_response(jsonify(state_objs), 200)
    else:
        obj = storage.get(State, state_id)
        if obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            return make_response(jsonify(obj.to_dict()), 200)

""" Method PUT """
@app_views.route('/states', methods=['PUT'], strict_slashes=False)
@app_views.route('/states/<state_id>')
def put_state(state_id):
    if state_id is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 404)
    else:
        obj = storage.get(State, state_id)
        if obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            data = request.get_json(silent=True, force=True)
            if data is None:
                return make_response(jsonify({'error': 'Not a JSON'}), 404)
            [setattr(obj, **data) for item in data if item != ('id', 'created_at', 'updated_at')]
            obj.save()
            return make_response(jsonify(obj), 200)

""" Method POST """
@app_views.route('/states', methods=['POST'], strict_slashes=False)               
def post_state():
    data = request.get_json(silent=True, force=True)
    if data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 404)
    else:
        if 'name' not in data:
            return make_response(jsonify({'error': 'Missing name'}), 400)

    obj = State(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)

""" Method DELETE """
@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """ Method DELETE """
    obj = storage.get(State, state_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)
