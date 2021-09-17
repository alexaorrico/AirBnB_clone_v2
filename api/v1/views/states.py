#!/usr/bin/python3
"""
    API view related to State objects that handles all the default
    actions.
"""
import requests
from api.v1.views import app_views
from models import storage
from models.state import State
import json
from werkzeug.exceptions import BadRequest, NotFound
from flask import Flask, request, jsonify, make_response, abort


@app_views.route('/states', methods=['GET'])
def list() -> json:
    """
    Retrieves the list of all State objects.

    Returns:
        json: List of State objects with status code 200.
    """
    states = storage.all(State)
    list = []
    for key, state in states.items():
        list.append(state.to_dict())
    return make_response(jsonify(list), 200)


@app_views.route('/states/<state_id>', methods=['GET'])
def show(state_id) -> json:
    """
    Retrieves a specified State object.

    Args:
        state_id : ID of the wanted State object.

    Raises:
        NotFound: Raises a 404 error if state_id
        is not linked to any State object.

    Returns:
        json: Wanted State object with status code 200.
    """
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    return make_response(jsonify(state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete(state_id) -> json:
    """
    Deletes a specified State object.

    Args:
        state_id : ID of the wanted State object.

    Raises:
        NotFound: Raises a 404 error if state_id
        is not linked to any State object.

    Returns:
        json: Empty dictionary with the status code 200.
    """
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)
