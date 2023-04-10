#!/usr/bin/python3

import json

from flask import abort, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'])
def states_list():
    """returns states list"""

    from models import storage
    from models.state import State

    dict_states = storage.all(State)
    proccesed_states = []

    for state in dict_states.values():
        proccesed_states.append(state.to_dict())
    return jsonify(proccesed_states)


@app_views.route('/states', methods=['POST'])
def post_state():
    from flask import request
    from models.state import State

    http_request = request.get_json(silent=True)
    if http_request == None:
        return 'Not a JSON', 400
    elif 'name' not in http_request.keys():
        return 'Missing name', 400

    new_state = State(**http_request)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """updates given state"""

    from flask import request
    from models.state import State

    found_state = storage.get(State, state_id)

    if found_state == None:
        return '', 404

    http_request = request.get_json(silent=True)
    if http_request == None:
        return 'Not a JSON', 400

    for key, values in http_request.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(found_state, key, values)

    storage.save()
    return jsonify(found_state.to_dict()), 201


@ app_views.route('/states/<state_id>', methods=['GET'])
def state_id(state_id):
    """GET state by id"""

    from models import storage
    from models.state import State

    dict_states = storage.all(State)

    for state in dict_states.values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@ app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """DELETE state id"""

    from models import storage
    from models.state import State

    dict_states = storage.all(State)

    for state in dict_states.values():
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    abort(404)
