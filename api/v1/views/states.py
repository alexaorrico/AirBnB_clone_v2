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
