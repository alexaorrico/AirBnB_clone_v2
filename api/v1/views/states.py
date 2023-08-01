#!/usr/bin/python3
'''module api/v1/views/states.py:
create a new view for State objects - handles all default RESTful API actions
'''
from flask import abort, jsonify, request

from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    '''GET /states
    Retrieves the list of all State objects
    '''
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    '''GET /states/<state_id>
    Retrieves a State object
    '''
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    '''DELETE /states/<state_id>
    Deletes a State object
    '''
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''POST /states
    creates a State object
    '''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    kwargs = request.get_json()
    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''PUT /states/<state_id>
    Updates a State object
    '''
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''404: Not Found'''
    return jsonify({'error': 'Not found'}), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''400:
    return Bad Request message for illegal requests to API
    '''
    return jsonify({'error': 'Bad Request'}), 400
