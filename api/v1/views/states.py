#!/usr/bin/python3
""" States """

from flask import jsonify, make_response, request
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrives all states objects"""
    objects = storage.all(State)
    list_values = []
    for key, value in objects.items():
        list_values.append(value.to_dict())
    return jsonify(list_values)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """ Get state by ID """
    state_object = storage.get(State, state_id)
    result = None
    if state_object.__class__.__name__ == 'State':
        result = jsonify(state_object.to_dict())
    else:
        result = abort(404)
    return result


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state_by_id(state_id):
    """ DELETE state by ID """
    state_object = storage.get(State, state_id)
    result = None
    if state_object.__class__.__name__ == 'State':
        storage.delete(state_object)
        storage.save()
        result = make_response(jsonify({}), 200)
    else:
        result = abort(404)
    return result


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """ ADD states """
    if request.is_json:
        data = request.get_json()
        if 'name' not in data:
            result = jsonify({'error': 'Missing name'}), 400
        else:
            new_object = State(**data)
            storage.new(new_object)
            storage.save()
            result = jsonify(new_object.to_dict()), 201
    else:
        result = jsonify({'error': 'Not a JSON'}), 400
    return result


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id):
    """ PUT states """
    state_object = storage.get(State, state_id)
    if not state_object.__class__.__name__ == 'State':
        return abort(404)
    if request.is_json:
        data = request.get_json()
        for key, value in data.items():
            setattr(state_object, key, value)
        storage.save()
        result = jsonify(state_object.to_dict()), 200
    else:
        result = jsonify({'error': 'Not a JSON'}), 400
    return result
