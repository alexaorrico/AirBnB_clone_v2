#!/usr/bin/python3
"""state file"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage, CNC


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def state():
    """
    function for state route that returns all the states in the database
    """
    if request.method == 'GET':
        all_state = storage.all("State")
        resp = []
        for a, b in all_state.items():
            resp.append(b.to_dict())
        return jsonify(resp)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get("name") is None:
            abort(400, 'Missing name')
        State = CNC.get("State")
        new_object = State(**req_json)
        new_object.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
# @app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
# strict_slashes=False)
def state_ids(state_id=None):
    """
    run directive base base on a given state id
    """
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(state_obj.to_dict())

    if request.method == 'DELETE':
        state_obj.delete()
        return jsonify({})

    if request.method == 'PUT':
        req_dict = request.get_json()
        if req_dict is None:
            abort(400, 'Not a JSON')
        state_obj.bm_update(req_dict)
        return jsonify(state_obj.to_dict())
