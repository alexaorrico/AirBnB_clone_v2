#!/usr/bin/python3
'''
Create a new view for State objects that
handles all default RESTFul API actions
'''

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request

@app_views.get('/states', strict_slashes=False)
def get_states():
    ''' Retrieves the list of all State objects '''
    states = storage.all(State).values()
    states = [state.to_dict() for state in states]
    return jsonify(states)

@app_views.get('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    ''' Retrieves a State object '''
    state = storage.get(State, state_id)
    print(type(state))
    if state is not None:
        return jsonify(state.to_dict())
    else:
        abort(404)
    

@app_views.delete('/states/<state_id>', strict_slashes=False)
def delete_state(state_id):
    ''' Deletes a State object '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.post('/states', strict_slashes=False)
def create_state():
    ''' Creates a State Object '''
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201

@app_views.put('/states/<state_id>', strict_slashes=False)
def update_state(state_id):
    ''' Updates a State Object '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
