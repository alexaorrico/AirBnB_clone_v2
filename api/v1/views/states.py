#!/usr/bin/python3
'''creates a new view for State objects'''
from models import storage
from api.v1.views import app_views
from models.state import State
from flask import jsonify, request, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getter_states():
    '''getter_states - gets all state objects'''
    new_list = []
    allstates = list(storage.all("State").values())

    for state in allstates:
        new_list.append(state.to_dict())
    return jsonify(new_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getter_id(state_id):
    '''getter_id - gets all state objects by id'''
    try:
        state = storage.get(State, state_id).to_dict()
        return jsonify(state)
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def deleter_id(state_id):
    '''deleter_id - delete an object by id'''
    id = storage.get(State, state_id)

    if id is not None:
        storage.delete(id)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    '''post_state - create an state object with post'''
    try:
        if not request.json():
            return jsonify({"error": "Not a JSON"}), 400
        body_dict = request.get_json()
        if "name" not in body_dict:
            return jsonify({"error": "Missing name"}), 400
        state = State(name=body_dict["name"])
        state.save()
        return jsonify(state.to_dict()), 201
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    '''put_state - updates a state object by id'''
    stateId = storage.get(State, state_id)

    if stateId is None:
        abort(404)
    body_dict = request.get_json()
    if body_dict is None:
        abort(400, "Not a JSON")
    body_dict.pop("id", None)
    body_dict.pop("created_at", None)
    body_dict.pop("updated_at", None)
    for key, value in body_dict.items():
        setattr(stateId, key, value)
    stateId.save()
    return jsonify(stateId.to_dict()), 200
