#!/usr/bin/python3
"""Endpoints for state"""

from flask import request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def allStatesList():
    """Retrieves the list of all State objects"""
    stateList = storage.all(State)
    return [obj.to_dict() for obj in stateList.values()]


@app_views.route('/states/<state_id>', strict_slashes=False)
def stateById(state_id):
    """Retrieves a State object with id = @state_id"""
    stateObj = storage.get(State, state_id)
    if stateObj is None:
        abort(404)
    return stateObj.to_dict()


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete State object with id = @state_id"""
    stateObj = storage.get(State, state_id)
    if stateObj is None:
        abort(404)
    storage.delete(stateObj)
    storage.save()
    return {}, 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createState():
    """Creates a new State object"""
    newStateDict = request.get_json()
    if not newStateDict:
        abort(400, 'Not a JSON')
    if not newStateDict.get('name'):
        abort(400, 'Missing name')
    newState = State()
    try:
        newStateDict.pop('id')
        newStateDict.pop('created_at')
        newStateDict.pop('updated_at')
    except KeyError:
        pass

    for key, value in newStateDict.items():
        setattr(newState, key, value)
    newState.save()
    return newState.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updateState(state_id):
    """Updates attributes of of State object"""
    stateObj = storage.get(State, state_id)
    if stateObj is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(stateObj, key, value)
    stateObj.save()
    return stateObj.to_dict(), 200
