#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """
    Retrieves the list of all State objects or a specific State
    ---
    title: HBNB State API
    info:
      description: This is the documentation for state API requests
    parameters:
      - name: state_id
        in: path
        type: string
        required: False
        description: the uuid of the state
    responses:
      404:
        description: Error resource not found
      200:
        description: Request executed successfully
    """

    if not state_id:
        all_states = storage.all(State).values()
        list_states = []
        for state in all_states:
            list_states.append(state.to_dict())
        return jsonify(list_states)
    else:
        state = storage.get(State, state_id)
        if not state:
            abort(404)

        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State Object
    ---
    parameters:
      - name: state_id
        in: path
        required: True
        description: uuid of the state
    responses:
      404:
        State not found
      200:
        State deletion was completed successfully
    """

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    Creates a State
    ---
    parameters:
      - name: name
        in: header
        requred: True
        description: The name of the state
    responses:
      404:
        State not found
      400:
        error: Not a valid JSON or Missing State name
      200:
        State deletion was completed successfully
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Updates a State
    ---
    parameters:
      - name: state_id
        in: path
        required: True
        description: uuid of the state
    responses:
      404:
        State not found
      200:
        State update was completed successfully
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
