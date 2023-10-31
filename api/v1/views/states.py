#!/usr/bin/python3
''''new view for State objects that handles all default RESTFul API actions'''


from models.state import State
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    '''Retrieves the list of all State objects'''
    states_ = storage.all(State).values()
    stateList = [state.to_dict() for state in states_]
    return jsonify(stateList)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    '''Retrieves a State object'''
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    '''Deletes a State object:'''
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''Creates a State'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    
    kwargs = request.get_json()
    if 'name' not in kwargs:
        abort(400, 'Missing name')
    
    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Updates a State'''
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, 'Not a JSON')

        jsonData = request.get_json()
        ignoreKeys = ['id', 'created_at', 'updated_at']

        for key, value in jsonData.items():
            if key not in ignoreKeys:
                setattr(state, key, value)
        
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(400)

@app_views.errorhandler(404)
def not_found(error):
    '''Raises 404 error'''
    res = {'error': 'Not found'}
    return jsonify(res), 404

@app_views.errorhandler(400)
def bad_request(error):
    '''Returns bad request message (illegal API requests)'''
    res = {'error': 'Bad Request'}
    return jsonify(res), 400
