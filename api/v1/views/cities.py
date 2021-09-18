#!/usr/bin/python3
"""
    API view related to City objects that handles all the default
    actions.
"""
import requests
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
import json
from werkzeug.exceptions import BadRequest, NotFound
from flask import Flask, request, jsonify, make_response, abort


def __is_valid_json(data):
    """
    Checks if the given data is a valid json.

    Args:
        data : Data to check

    Returns:
        True: If data is a valid json.
        False: If data is not a valid json.
    """
    try:
        json.loads(data)

        return True
    except Exception:
        return False


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def Cities_list(state_id) -> json:
    """
    Retrieves the list of all City objects.

    Returns:
        json: List of City objects with status code 200.
    """
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    list = []
    for city in state.cities:
        list.append(city.to_dict())
    return make_response(jsonify(list), 200)
