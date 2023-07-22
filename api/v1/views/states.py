#!/usr/bin/python3
""" Create a new view for State objects that handles all default
RestFul API actions which are: GET, DELETE, POST, PUT """

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


# GET /api/v1/states
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


# GET /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object by its state_id"""
    state = storage.get(State, state_id)
    if state is None:
        # If the state_id is not linked to any State object, raise a 404 error
        abort(404)
    # Convert the State object to a dictionary and return it as JSON response
    return jsonify(state.to_dict())


# DELETE api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object based on the state_id
    if state doesn't exist, raise a 404 error, delete it,
    return an empty dictionary with the status code 200"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


# POST api/v1/states
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    Creates a State object based on the JSON body request.
    if the JSON body request is not valid, raise a 400 error.
    if the JSON body request does not contain the key name, raise a 400 error.
    return a dictionary representation of the new
    State object with a status code 201
    """
    # If the JSON body request is not valid, raise a 400 error
    if not request.get_json():
        # abort() will raise an exception that returns a response
        abort(400, description="Not a JSON")
    # If the JSON body request does not contain the key name, raise a 400 error
    if 'name' not in request.get_json():
        # abort() will raise an exception that returns a response
        abort(400, description="Missing name")
    # ** unpacks the dictionary *args *kwargs
    # State(**request.get_json()) returns a State object by unpacking the dict
    # and passing it as a keyword arguments to the State constructor
    new_state = State(**request.get_json())
    # save the new state
    new_state.save()
    # return a dictionary representation of the new State object with a status
    return jsonify(new_state.to_dict()), 201


# PUT api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Updates a State object based on the state_id
    if the JSON body request is not valid, raise a 400 error.
    if the State object doesn't exist, raise a 404 error.
    return a dictionary representation of the State object with the status code
    200
    """
    state = storage.get(State, state_id)
    # If the state_id is not linked to any State object, raise a 404 error
    if state is None:
        # abort() will raise an exception that returns a response
        abort(404)
    # If the JSON body request is not valid, raise a 400 error
    if not request.get_json():
        abort(400, description="Not a JSON")
    # Update the State object with all key-value pairs of the dictionary
    for key, value in request.get_json().items():
        # if key is not in the list, ignore it
        if key not in ['id', 'created_at', 'updated_at']:
            # setattr(object, name, value) is the same as state.key = value
            setattr(state, key, value)
    # save the updated state
    state.save()
    # return a dictionary representation of the State object with the status
    return jsonify(state.to_dict()), 200

""" run the following commands to test this view:
HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 python3 -m api.v1.app
curl -X GET http://
"""
