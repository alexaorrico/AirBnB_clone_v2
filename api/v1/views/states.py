#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def Getstates():
    """
    Retrieves the list of all State objects
    """
    if request.method == 'GET':
        states = []
        for state in storage.all("State").values():
            states.append(state.to_dict())
        return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def Getstate(state_id):
    """
    Retrieves a State object using specific id otherwise 404
    """
    if request.method == 'GET':
        state = storage.get('State', state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def Deletestate(state_id):
    """
    Deletes a State object based on its state_id otherwise 404
    """
    if request.method == 'DELETE':
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        state.delete()
        storage.save()
        return (jsonify({}))


@app_views.route('/states/', methods=['POST'])
def Poststate():
    """
    creates a state
    """
    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({'error': 'Missing name'}), 400)
        state = State(**request.get_json())
        state.save()
        return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def Putstate(state_id):
    """
    updates a state object
    """
    if request.method == 'PUT':
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in request.get_json().items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(state, attr, val)
        state.save()
        return jsonify(state.to_dict())
