#!/usr/bin/python3
"""
Defines a RESTful API view for State objects.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger import Swagger, swag_from
from models import storage, CNC


@app_views.route('/states', methods=['GET', 'POST'])
@swag_from('swagger_yaml/states_no_id.yml', methods=['GET', 'POST'])
def states_no_id():
    """
    Handle GET and POST requests for State objects without specifying an ID.
    """
    if request.method == 'GET':
        all_states = storage.all('State')
        all_states = [obj.to_json() for obj in all_states.values()]
        return jsonify(all_states)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None or req_json.get("name") is None:
            abort(400, 'Invalid JSON or missing name')
        State = CNC.get("State")
        new_object = State(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/states_id.yml', methods=['PUT', 'GET', 'DELETE'])
def states_with_id(state_id=None):
    """
    Handle GET, DELETE, and PUT requests for a specific State object by ID.
    """
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'State not found')

    if request.method == 'GET':
        return jsonify(state_obj.to_json())

    if request.method == 'DELETE':
        state_obj.delete()
        return jsonify({})

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Invalid JSON')
        state_obj.bm_update(req_json)
        return jsonify(state_obj.to_json())
