#!/usr/bin/python3
"""
handles all default RestFul API actions for states
"""

from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def view_all_states():
    """Example endpoint returning a list of all the states
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
            items:
              $ref: '#/definitions/Color'

      Color:
        type: string
    responses:
      200:
        description: A list of dictionarys, each dict is a State
        schema:
          $ref: '#/definitions/State'
        examples:
            [{'__class__': 'State', 'created_at': '2017-03-25T02:17:06',
            'id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f', 'name': 'Oregon',
            'updated_at': '2017-03-25T02:17:06'}]

    """
    all_states = storage.all("State")
    states = []
    for state in all_states.values():
        states.append(state.to_json())
    return jsonify(states)


@app_views.route('/states/<int:state_id>',
                 methods=['GET'], strict_slashes=False)
def view_one_state(state_id=None):
    """Example endpoint returning a list of one state
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
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of one dictionary of the desired State object
        schema:
          $ref: '#/definitions/State'
        examples:
            [{'__class__': 'State', 'created_at': '2017-03-25T02:17:06',
            'id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f', 'name': 'Oregon',
            'updated_at': '2017-03-25T02:17:06'}]

    """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_json())


@app_views.route('/states/<int:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def remove_state(state_id):
    """
    Example endpoint deleting one state
    Deletes a state based on the state_id
    ---
    definitions:
      State:
        type: object
      Color:
        type: string
      items:
        $ref: '#/definitions/Color'

    responses:
      200:
        description: An empty dictionary
        schema:
          $ref: '#/definitions/State'
        examples:
            {}
    """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Example endpoint creating a state
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
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      201:
        description: A list of a single dictionary of a State
        schema:
          $ref: '#/definitions/State'
        examples:
            [{'__class__': 'State', 'created_at': '2017-03-25T02:17:06',
            'id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f', 'name': 'Oregon',
            'updated_at': '2017-03-25T02:17:06'}]
    """
    body = None
    try:
        body = request.get_json()
    except BaseException:
        body = None
    if body is None:
        abort(400, "Not a JSON")
    if 'name' not in body.keys():
        abort(400, "Missing name")
    state = State(**body)
    state.save()
    return jsonify(state.to_json()), 201


@app_view.route('/states/<int:state_id>',
                methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    update state
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
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      201:
        description: A list of a single dictionary of a State
        schema:
          $ref: '#/definitions/State'
        examples:
            [{'__class__': 'State', 'created_at': '2017-03-25T02:17:06',
            'id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f', 'name': 'Oregon',
            'updated_at': '2017-03-25T02:17:06'}]
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    try:
        body = request.get_json()
    except BaseException:
        body = None
    if body is None:
        abort(400, "Not a JSON")
    for key, value in body.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_json()), 200
