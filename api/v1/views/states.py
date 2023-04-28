#!/usr/bin/python3
"""

"""


from api.v1.views import app_views
from models import storage, State
from flask import jsonify, request, abort


@app_views.route('/states', methods=['GET'])
def get_states():
    """ """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ """
    state = storage.get(State, state_id)

    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """"""
    state = storage.get(State, state_id):

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/states', methods=['POST'])
def create_state():
    """"""
    data = request.get_json()
    
    if not data():
        abort(400, description="Not a JSON")

    name = data.get('name')
    if not name:
        abort(400, description="Missing name")

    state = State(name=name)
    state.save()

    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')

    ignore_keys = {'id', 'created_at', 'updated_at'} 
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    state.save()

    return make_response(jsonify(state.to_dict()), 200)
