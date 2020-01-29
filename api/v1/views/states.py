#!/usr/bin/python3
"""
States file for APi project
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def list_states():
    """lists all states"""
    s_list = []
    states = storage.all("State")
    for state in states.values():
        s_list.append(state.to_dict())
    return jsonify(s_list)

@app_views.route('/states/<state_id>', methods=['GET'])
def GetStateById(state_id):
    """Retrieves state based on its id for GET HTTP method"""
    all_states = storage.all("State")
    for state in all_states.values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def DeleteStateById(state_id):
    """Deletes an state based on its id for DELETE HTTP method"""
    exists = False
    all_states = storge.all("State")
    for state in all_states.values():
        if state.id == state_id:
            exists = True
            storage.delete(state)
            return {}
    storage.save()
    if not exists:
        abort(404)

@app_views.route('/states/<state_id>', methods=['POST'])
def PostState()

if __name__ == '__main__':
    pass
