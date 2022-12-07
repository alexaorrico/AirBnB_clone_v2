#!/usr/bin/python3
"""view of State object"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort
from models.state import State


# Retrieves the list of all State objects: GET /api/v1/states
@app_views.route('/states/', strict_slashes=False)
# Retrieves a State object: GET /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """ Return all states """
    if state_id is None:
        new_dict = [state.to_dict() for state in storage.all(State).values()]
        return jsonify(new_dict)
    else:
        """ Return a State object """
        new_dict = storage.get(State, state_id)
        if new_dict is None:
            abort(404)
        return jsonify(new_dict.to_dict())
