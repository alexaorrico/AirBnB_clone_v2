#!/usr/bin/python3
""" API view for State objects. """
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'])
def all_states(text="is-cool"):
    """ Returns list of all State objs. """
    all_states = storage.all(State)
    list_all_states = []
    for state in all_states:
        list_all_states.append(all_states[state].to_dict())
    return jsonify(list_all_states)

@app_views.route('/states/<string:id>', methods=['GET'])
def get_state(id):
    """ Returns the State obj in JSON. """
    state = storage.get(State, id)
    if not state:
        abort(404)
    return jsonify(state["State.{}".format(id)].to_dict())

@app_views.route('/states/<string:id>', methods=['DELETE'])
def delete_state(id):
    """ Deletes the State obj from storage. """
    deleted = {}
    storage.delete(storage.get(State, id)["State.{}".format(id)])
    return jsonify(deleted), 200

@app_views.route('/states', methods=['POST'])
def create_state(text="is_cool"):
    """ Creates a new State obj. """
    if not request.json or not 'name' in request.json:
        abort(404)
    print(request.json['name'])
    storage.new(State({'name': request.json['name']}))
    storage.save()
    return jsonify(state.to_dict())
