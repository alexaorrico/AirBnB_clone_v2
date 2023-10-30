#!/usr/bin/python3
"""
API State View Module

Defines the API views for the state objects, providing RESTful
endpoints to interact with state resources.

Endpoints:
- GET /api/v1/: Retrieves a list of all objects.
- GET /api/v1/states/<state_id>: Retrieves an object by its ID.
- DELETE /api/v1/states/<state_id>: Removes an object by its ID.
- POST /api/v1/states: Creates a new object.
- PUT /api/v1/states/<state_id>: Updates an object by its ID.

Each endpoint performs specific actions on state resources and returns
results in JSON format.

HTTP status codes:
- 200: OK: The request has been successfully processed.
- 201: 201 Created: The new resource has been created.
- 400: Bad Request: The server cannot process the request.
- 404: Not Found: The requested resource could not be found on the server.
"""

from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves a list of all State objects """
    states_dict = storage.all(State)
    states_list = []
    for elem in states_dict.values():
        states_list.append(elem.to_dict())
    return jsonify(states_list)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a new State object """
    if not request.get_json():
        abort(400, description='Not a JSON')
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    query = request.get_json()
    new = State(**query)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object by its ID """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Remove a State object by its ID """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Update a State object by its ID """
    if not storage.get(State, state_id):
        abort(404)
    if request.content_type != 'application/json':
        abort(400, description='Not a JSON')
    state = storage.get(State, state_id)
    query = request.get_json()
    ignore_list = ['id', 'created_at', 'updated_at']
    for key, val in query.items():
        if key not in ignore_list:
            setattr(state, key, val)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
