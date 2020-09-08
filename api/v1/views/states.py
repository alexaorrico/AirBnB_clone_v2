#!/usr/bin/python3
"""sturts"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify


@app_views.route('/api/v1/states', methods=['GET'])
def get_states():
    """returns list of all states"""
    lizt = []
    states = storage.all(State).values()
    for state in states:
        lizt.append(state.to_dict())
    return jsonify(lizt)

@app_views.route('/api/v1/states/<state_id>')
def get_a_state():
    """finds a unique state based of state_id"""
    lizt = []
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            lizt = state.to_dict()
            return jsonify(lizt)
    return jsonify({"error": "Not found"}), 404
    """MENTAL NOTE:  maybe a try/except block"""

@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_a_state():
    """delete a specific state"""
    lizt = []
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    return jsonify({'error': 'Not found'}), 404

@app_views.route('/api/v1/states', methods=['POST'])
def create_a_state():
    """create a state"""
    req = request.get_json()
    if req is not (type)JSON:
        raise TypeError(400, 'Not a JSON')
    key = 'name'
    if key not in req:
        raise ValueError(400, 'Missing name')
    new_state = State(**req)
    new_state.save()
    return jsonify(new_state), 201

@app_view.route('/api/v1/states/<state_id>', methods=['PUT'])
def update_a_state():
    """ this method updates a state """
    states = storage.all(State).values()
    req = request.get_json()
    if req is not (type)JSON:
        raise TypeError(400, 'Not a JSON')
    for state in states:
        if state.id not in states:
        """ ^^ NOTE: should this be state_id ??? ^^ """
            raise KeyError(404, 'state_id not found')
        else:
            for key, value in states:
                if key is not 'id' or key is not 'created_at'
                or key is not 'updated_at':
                    states.update({'key':'value'})
                return jsonify(states), 200

                """A DIFFERENT APPROACH:
                if key == '__class__':
                    states['__class__'] = value
                if key == 'name':
                    states['name'] = value"""
