#!/usr/bin/python3
"""api states"""
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """retrieves all State object"""
    allStates = storage.all(State).values()
    statesList = []
    for state in allStates:
        statesList.append(state.to_dict())
    return statesList
