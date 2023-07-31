#!/usr/bin/python3
"""
module state.py
"""

from flask import abort, jsonify, request, make_response
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


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def stateObjectWithId(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def stateDeleteWithId(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createState():
    """Creates a State: POST /api/v1/states"""
    if request.headers.get('Content-Type') != "application/json":
        abort(400, "Not a JSON")

    newStateData = request.get_json()

    if not newStateData.get("name"):
        abort(400, "Missing name")

    newStateObj = State(**newStateData)
    """newStateObj.save()"""
    storage.new(newStateObj)
    storage.save()

    return make_response(jsonify(newStateObj.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def updateState(state_id):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    if not request.is_json:
        abort(400, "Not a JSON")

    stateUpdateData = request.get_json()
    stateObj = storage.get(State, state_id)
    if stateObj:
        ignoredKeys = ['id', 'created_at', 'updated_at']
        for k, v in stateUpdateData.items():
            if k not in ignoredKeys:
                setattr(stateObj, k, v)
        storage.save()
        return make_response(jsonify(stateObj.to_dict()), 200)
    else:
        abort(404)
