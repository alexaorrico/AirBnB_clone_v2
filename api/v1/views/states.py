#!/usr/bin/python3
''' States viewer '''

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getStates():
    ''' gets all State information used for all states '''
    statesList = []
    for state in storage.all("State").values():
        statesList.append(state.to_dict())
    return jsonify(statesList)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def getState(state_id):
    ''' gets State information for named state '''
    stateSelect = storage.get("State", state_id)
    if stateSelect is None:
        abort(404)
    return jsonify(stateSelect.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteState(state_id):
    ''' deletes named state based on its state_id '''
    stateDelete = storage.get("State", state_id)
    if stateDelete is None:
        abort(404)
    stateDelete.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def postState():
    ''' create a new state '''
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    statePost = State(**request.get_json())
    statePost.save()
    return make_response(jsonify(statePost.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def putState(state_id):
    ''' updates named state '''
    stateUpdate = storage.get("State", state_id)
    if stateUpdate is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, value in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(stateUpdate, attr, value)
    stateUpdate.save()
    return jsonify(stateUpdate.to_dict())
