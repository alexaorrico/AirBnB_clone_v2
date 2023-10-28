#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response. request
from models import storage, CNC


@app_views.route('/states', methods=['GET', 'POST'])
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states(state_id=None):
    """
    States route to handle http method for requested state/s
    """
    all_states = storage.all('State')
    fetch_string = "{}.{}".format('State', state_id)
    state_obj = all_states.get(fetch_string)

    if request.method == 'GET':
        if state_id:
            if state_obj:
                return jsonify(state_obj.to_json())
            else:
                abort(404, 'Not found')
        else:
            all_states = list(obj.to_json() for obj in all_states.values())
            return jsonify(all_states)

    if request.method == 'DELETE':
        if state_obj:
            state_obj.delete()
            del state_obj
            return jsonify({})
        abort(404, 'Not found')

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get("name") is None:
            abort(400, 'Missing name')
        State = CNC.get("State")
        new_object = State(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201

    if request.method == 'PUT':
        req_json = request.get_json()
        if state_obj is None:
            abort(404, 'Not found')
        if req_json is None:
            abort(400, 'Not a JSON')
        state_obj.bm_update(req_json)
        return jsonify(state_obj.to_json())
