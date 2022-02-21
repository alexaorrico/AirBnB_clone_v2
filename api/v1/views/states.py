#!/usr/bin/python3
"""states api view module"""
from email.policy import strict
from api.v1.views import app_views
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from models import storage
from models.state import State  # state model


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """
        Example endpoint returning a list of all the states
    Retrieves a list of all the states
    ---
    definitions:
      State:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          id:
            type: string
            description: the id of the state
          name:
            type: string
            description: name of the state
          updated_at:
            type: string
            description: The date the object was updated

    responses:
      200:
        description: A list of dictionarys, each dict is a State
    """
    all_states = [state.to_dict() for state in storage.all('State').values]
    return jsonify(all_states), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """
    Retrieves a state by a given id
    ---
    parameters:
      - name: state_id
        in: path
        type: string
        enum: ['None', '10098698-bace-4bfb-8c0a-6bae0f7f5b8f']
        required: true
        default: None
    definitions:
      State:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          id:
            type: string
            description: the id of the state
          name:
            type: string
            description: name of the state
          updated_at:
            type: string
            description: The date the object was updated

    responses:
      200:
        description: A list of one dictionary of the desired State object
        """
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)  # get state object
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)


def delete_state(state_id=None):
    """
    Retrieves a state by a given id
    ---
    parameters:
      - name: state_id
        in: path
        type: string
        enum: ['None', '10098698-bace-4bfb-8c0a-6bae0f7f5b8f']
        required: true
        default: None
    definitions:
      State:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          id:
            type: string
            description: the id of the state
          name:
            type: string
            description: name of the state
          updated_at:
            type: string
            description: The date the object was updated

    responses:
      200:
        description: A list of one dictionary of the desired State object
    """
    if state_id is None:
        abort(404)
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State object based on the JSON body
    ---
    definitions:
      State:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          id:
            type: string
            description: the id of the state
          name:
            type: string
            description: name of the state
          updated_at:
            type: string
            description: The date the object was updated

    responses:
      201:
        description: A list of a single dictionary of a State
    """
    try:
        kwargs = request.get_json()
    except None:
        return "Not a JSON", 400

    if 'name' not in kwargs.keys():
        return 'Missing name', 400

    state = State(**kwargs)
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], stric_slashes=False)
def update_state(state_id=None):
    """
    Updates a State object based on the JSON body
    ---
    parameters:
      - name: state_id
        in: path
        type: string
        enum: ['None', '10098698-bace-4bfb-8c0a-6bae0f7f5b8f']
        required: true
        default: None
    definitions:
      State:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          id:
            type: string
            description: the id of the state
          name:
            type: string
            description: name of the state
          updated_at:
            type: string
            description: The date the object was updated

    responses:
      201:
        description: A list of a single dictionary of a State
    """
    try:
        kwargs = request.get_json()
    except None:
        return "Not a JSON", 400

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for k in ("id", "created_at", "updated_at"):
        kwargs.pop(k, None)
    for k, v in kwargs.items():
        setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
