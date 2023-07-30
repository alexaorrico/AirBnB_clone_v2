#!/usr/bin/python3
"""
module state.py
"""

from flask import abort, jsonify
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def stateObjects():
    """ Retrieves the list of all State objects: GET /api/v1/states """
    states = storage.all(State)
    statesList = []
    for state in states.values():
        """print (state)"""
        stateDict = state.to_dict()
        statesList.append(stateDict)    
    """states_list = [state.to_dict() for state in states.values()]"""
    return jsonify(statesList)


@app_views.route('/states/<int:state_id>', methods=['GET'], strict_slashes=False)
def stateObjectWithId(id):
    """Retrieves a State object"""
    states = storage.all(State)
    for state in states.values():
        for value in state.values():
            if id == value:
                stateDict = state.to_dict()
                print (value)
                print (state)
                return jsonify(stateDict)
