#!/usr/bin/python3
"""
module that defines API interactions for State __objects
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """
    defines the states route
    Returns: list of all State objects
    """
    states = storage.all("State").values()

    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["GET"])
def id_for_state(state_id):
    """
    defines the states/<state_id> route
    Returns: state id or 404 Error if object not linked to State object
    """
    a_state = storage.get("State", state_id)
    if a_state:
        return jsonify(a_state.to_dict())
    return abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state_id(state_id):
    """
    defines DELETE for state objects by id
    Returns: if successful 200 and an empty dictionary
             404 if state_id is not linked to any State obj
    """
    state = storage.get("State", state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/states/', strict_slashes=False, methods=['POST'])
def create_state():
    """
    define how to create a new state objects
    Returns: 201 on successful creation
             400 "Not a JSON" if HTTP body request is not valid
             404 if state_id is not linked to any State object
    """
    try:
        states = request.get_json()

        if states.get("name") is None:
            return abort(400, 'Missing name')
    except:
        return abort(400, 'Not a JSON')

    new_state = State(**states)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def state_update(state_id):
    """
    defines how an Update to a state is made
    Returns: 200 and the state object if successful
             400 "Not a JSON" if HTTP body request is not valid
             404 if state_id is not linked to any State object
    """
    state_data = request.get_json()

    if not state_data:
        return abort(400, 'Not a JSON')

    state = storage.get("State", state_id)

    if not state:
        return abort(404)

    for key, value in state_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()

    return jsonify(state.to_dict()), 200
