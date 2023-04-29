#!/usr/bin/python3
"""A scripts that handle RestAPI action for state"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, CNC


@app_views.route('/states', methods=['GET', 'POST'])
def State():
    """Route that fetch/Add State Objects"""
    if request.method == 'GET':
        states = storage.all('State')
        states_list = list(state.to_json() for state in states.values())
        return jsonify(states_list)
    if request.method == 'POST':
        request_json = request.get_json()
        if request_json is None:
            abort(404, 'Not a JSON')
        if request_json.get("name") is None:
            abort(400, 'Missing Name')
        State = CNC.get("State")
        new_state_obj = State(**request_json)
        new_state_obj.save()
        return jsonify(new_state_obj.to_json()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def get_state_by_id(state_id):
    """Route that handles retrieving and deleteing
       a state base on the state id
       Parameter:
        state_id: string, state id to retrieve or delete
       Return:
        GET - The retrived state in json
        DELETE - empty json
        PUT: updated state object
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        return jsonify(state.to_json())
    if request.method == 'DELETE':
        state.delete()
        del state
        return jsonigy({})
    if request.method == 'PUT':
        request_json = request.get_json()
        if request_json is None:
            abort(400, 'Not a JSON')
        state = bm_update(request_json)
        return jsonify(state.to_json()), 200
