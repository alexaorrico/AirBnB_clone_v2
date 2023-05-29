#!/usr/bin/python3
"""a new view for State objects that handles all default
RESTFul API actions"""

import os
from models import storage, State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states", strict_slashes=False, methods=['GET', 'POST'])
@swag_from(os.getcwd() + '/api/v1/views/apidoc/states_get.yaml',
           methods=['GET'])
@swag_from(os.getcwd() + '/api/v1/views/apidoc/states_post.yaml',
           methods=['POST'])
def all_states():
    """
	GET:Retrieves the list of all State objects
    POST:Creates a new state
	"""
	if request.methd == 'POST':
	    state_dict=request.get_json()
		if state_dict is None:
		    return 'Not a JSON', 400
		if 'name' not in state_dict.keys():
		    return 'Missing name', 400
		my_state = State(**state_dict)
        my_state.save()
        return jsonify(my_state.to_dict()), 201
    my_states = [state.to_dict() for state in storage.all('State').values()]
    return jsonify(my_states)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
@swag_from(os.getcwd() + '/api/v1/views/apidoc/states_state-id_get.yaml',
           methods=['GET'])
@swag_from(os.getcwd() + '/api/v1/views/apidoc/states_state-id_delete.yaml',
           methods=['DELETE'])
@swag_from(os.getcwd() + '/api/v1/views/apidoc/states_state-id_put.yaml',
           methods=['PUT'])
def get_state(state_id):
    '''
        GET: display a specific state
        DELETE: delete a state
        PUT: update a state
    '''
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(my_state)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        state_dict = request.get_json()
        if state_dict is None:
            return 'Not a JSON', 400
        for key, value in state_dict.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(my_state, key, value)
        my_state.save()
    return jsonify(my_state.to_dict())
