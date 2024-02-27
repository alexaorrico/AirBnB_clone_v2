#!/usr/bin/python3
"""flask return json response"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, classes


@app_views.route('/states', methods=['GET', 'POST'])
def states_no_id():
    """
        handle http method with no id provided for state request
    """
    if request.method == 'GET':
        states = storage.all('State')
        states = list(obj.to_json() for obj in states.values())
        return jsonify(states)

    if request.method == 'POST':
        json_request = request.get_json()
        if json_request is None:
            abort(400, 'Not a JSON')
        if json_request.get("name") is None:
            abort(400, 'Missing name')
        State = classes.get("State")
        new_object = State(**json_request)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states_with_id(state_id=None):
    """
        handle http method with id provided for state request
    """
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(state_obj.to_json())

    if request.method == 'DELETE':
        state_obj.delete()
        del state_obj
        return jsonify({})

    if request.method == 'PUT':
        json_request = request.get_json()
        if json_request is None:
            abort(400, 'Not a JSON')

        for k, v in json_request.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(state_obj, k, v)
        state_obj.save()
        return jsonify(state_obj.to_dict())
