#!/usr/bin/python3
"""
Module for State objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', defaults={'state_id': None}, methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def states(state_id):
    """ Retrieves the list of all State objects """
    if state_id is None:
        states_list = []
        for value in storage.all(State).values():
            states_list.append(value.to_dict())
        return jsonify(states_list)
    else:
        try:
            state_dic = storage.get(State, id).to_dict()
            return jsonify(state_dic)
        except:
            abort(404)
    
@app_views.route('/states', methods=['POST'])
def create_state():
    data = request.get_json()
    print(data)
    new_state = State(data)
    storage.new(new_state)
    storage.save()
    print(new_state)
    return jsonify(new_state.to_dict())
    """ try:
    except:
        abort(400)"""


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    try:
        state_dic = {}
        state_dic = storage.delete(storage.get(State, state_id))
        return jsonify(state_dic)
    except:
        abort(404)