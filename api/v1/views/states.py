#!/usr/bin/python3
'''Contains the states view for the API.'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a new state object """

    # if body doesn't contain valid JSON
    if not request.is_json:
        abort(400, "Not a JSON")

    # else transform HTTP body into a dict
    body = request.get_json()

    # if the name key doesnt exist in the body dict
    if body.get("name") is None:
        abort(400, "Missing name")

    # create and save the new state instance
    new_state = State(**body)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_states():
    """ Retrieves a list of all State objects """
    # grab all state objects from storage
    states = storage.all(State).values()

    # convert all state objects into dictionaries & put in list
    state_list = [state.to_dict() for state in states]

    # return the jsonified list
    return jsonify(state_list)


@app_views.route('/states/<id>', methods=['GET'], strict_slashes=False)
def retrieve_state(id):
    """ Retrieves a single State object based on its id """
    # grab the state object from storage
    state = storage.get(State, id)

    if state:  # return the jsonified object
        return jsonify(state.to_dict())
    else:  # else if state is None
        abort(404)


@app_views.route('/states/<id>', methods=['PUT'], strict_slashes=False)
def update_state(id):
    """ Updates specific instance of a state """
    # retrieve the object by id if it exists
    state = storage.get(State, id)

    # abort if state with specific id can't be found
    if state is None:
        abort(404)

    # if body doesn't contain valid JSON
    if not request.is_json:
        abort(400, "Not a JSON")

    # else transform HTTP body into a dict
    body = request.get_json()

    # ignore id, created_at, updated_at keys during update
    excluded_keys = ["id", "created_at", "updated_at"]
    # iterate over body dict & update the state object
    # with the new values from body dict
    for key, value in body.items():
        if key not in excluded_keys:
            setattr(state, key, value)

    # save the updated state instance
    storage.save()

    return jsonify(state.to_dict()), 200


@app_views.route('/states/<id>', methods=['DELETE'], strict_slashes=False)
def delete_state(id):
    """ Deletes specific instance of a state """
    # retrieve the object by id if it exists
    state = storage.get(State, id)

    # delete the object if it exists
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:  # else if state is None
        abort(404)
