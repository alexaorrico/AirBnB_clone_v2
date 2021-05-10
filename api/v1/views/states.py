#!/usr/bin/python3
"""
Flask route that returns status of state JSON object response in app_views
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states_not_linked():
    """states not linked to an object
    """
    if request.method == 'GET':
        all_state = [state.to_dict() for state in storage.
                     all('State').values()]
        return (jsonify(all_state), 200)
    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_linked(state_id=None):
    """states linked to JSON object
    """
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(state_obj.to_dict())

    if request.method == 'DELETE':
        state_obj.delete()
        storage.save()
        return (jsonify({}), 200)

    if request.method == 'PUT':
        if request.get_json() is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, value in request.get_json().items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(state_obj, attr, value)
    state_obj.save()
    return jsonify(state_obj.to_dict())
