#!/usr/bin/python3
""" New view for State objects that handles all default RESTFull Api actions :
        GET /states
        GET /states/state_id
        DELETE /states/state_id
        POST /states
        PUT /states/state_id

 """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """
        retrieves list of all State
    """
    # empty list to stock states
    all_states = []
    # load storage.all(State) and add values in empty list
    for obj in storage.all(State).values():
        all_states.append(obj.to_dict())
    # return json
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """
        retrieve specific state with given id
    """
    # get state with id
    state = storage.get(State, state_id)
    # if no given state -> Error 404
    if state is None:
        abort(404)
    else:
        # transform object in valid json
        stateID = state.to_dict()
    return jsonify(stateID)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
        delete specific state with given id
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
        create State
    """
    #  transform the HTTP body request to a dictionary
    json_data = request.get_json()
    if not json_data:
        return (jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in json_data:
        return (jsonify({"error": "Missing name"}), 400)
    # State(**kwargs)
    newstate = State(**json_data)
    newstate.save()
    # transform object in valid json
    newstate_dict = newstate.to_dict()
    return (jsonify(newstate_dict), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
        update State
    """
    #  transform the HTTP body request to a dictionary
    json_data = request.get_json()
    if not json_data:
        return (jsonify({"error": "Not a JSON"}), 400)

    # get given state
    given_state = storage.get(State, state_id)
    # if no State with right id
    if given_state is None:
        abort(404)

    # replace
    for key, value in json_data.items():
        # update item except this 3
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(given_state, key, value)

    storage.save()
    # transform object in valid json
    newstate_dict = given_state.to_dict()
    return (jsonify(newstate_dict), 200)
