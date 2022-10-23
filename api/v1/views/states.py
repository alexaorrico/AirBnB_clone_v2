

#!/usr/bin/python3
"""Module containing views for State objects """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects
    Returns:
        A list of dictionaries representing State Objects in JSON format.
    """
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id=None):
    """ Retrieves a state object by state_id
        Args:
            state_id (str): The UUID4 string representing a State object.
        Returns:
            A state object in JSON format.
            Raise 404 error if no match for state_id is found.
    """
    if state_id:
        for state in storage.all("State").values():
            if state.id == state_id:
                return jsonify(state.to_dict())
        abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id=None):
    """ Deletes a state object by state_id
        Args:
            state_id (str): The UUID4 string representing a State object.
        Returns:
            An empty dictionary with the status code 200.
            Raise 404 error if no match for state_id is found.
    """
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    state_obj.delete()
    storage.save()
    return jsonify({}), 200
