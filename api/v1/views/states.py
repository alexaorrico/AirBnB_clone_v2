#!/usr/bin/python3
from flask import request, jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def list_states():
    """
    Retrieves the list of all State objects: GET /api/v1/states
    Creates a State: POST /api/v1/states
    """
    if request.method == 'GET':
        list_states = []
        states = storage.all('State').values()
        for state in states:
            list_states.append(state.to_dict())
        return jsonify(list_states)
