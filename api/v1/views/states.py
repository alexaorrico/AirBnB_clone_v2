#!/usr/bin/python3
""" A new view that handles all default api actions to the state """
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """ A route on the endpoint that returns all the states """
    states = storage.all(State).values()
    all_states = []
    for state in states:
        all_states.append(state.to_dict())
    return jsonify(all_states), 200


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state_by_id(state_id):
    """ A route that retrieves the state based on the state id """
    all_states = storage.all(State).values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    return jsonify(state_obj[0])


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_object(state_id):
    """ A route that deletes a state based on the state id"""
    all_states = storage.all(State).values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    state_obj.remove(state_obj[0])
    for obj in all_states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_objects():
    """ A route that allows addition of states to the storage"""

    if not request.json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = []
    new = State(name=request.json['name'])
    storage.new(new)
    storage.save()
    states.append(new.to_dict())
    return jsonify(states[0]), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """ A route to update a specific state based on the state id"""
    all_states = storage.all(State).values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state_obj[0]['name'] = request.json['name']
    for obj in all_states:
        if obj.id == state.id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_obj[0]), 200
