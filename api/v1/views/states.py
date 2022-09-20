#!/usr/bin/python3
"""
flask application module for retrieval of
State Objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects"""
    return (jsonify(
            [obj.to_dict() for obj in storage.all("State").values()]))

@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieves a State object: state_id"""
    stateToReturn = storage.get("State", state_id)
    if stateToReturn is None:
        abort(404)
    return (jsonify(stateToReturn.to_dict()))

@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """Deletes a State object: state_id"""
    stateToDelete = storage.get("State", state_id)
    if stateToDelete is None:
        abort(404)
    stateToDelete.delete()
    storage.save()
    return (jsonify({}))

@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """create a new state object in DB"""
    newStateData = request.get_json()
    if newStateData is None or type(newStateData) != dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    new_name = newStateData.get('name')
    if new_name is None:
        return (jsonify({'error': 'Missing name'}), 400)
    newState = State(**newStateData)
    newState.save()
    return (jsonify(newState.to_dict()), 201)

@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state_by_id(state_id):
    """Updatea a State object: state_id"""
    putStateData = request.get_json()
    if putStateData is None or type(putStateData) != dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    stateToUpdate = storage.get("State", state_id)
    if stateToUpdate is None:
        abort(404)
    keysToIgnore = ['id', 'created_at', 'updated_at']
    for key, value in putStateData.items():
            if key in keysToIgnore:
                continue
            setattr(stateToUpdate, key, value)
    stateToUpdate.save()
    return (jsonify(stateToUpdate.to_dict()), 200)
