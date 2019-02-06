#!/usr/bin/python3
from api.v1.views import app_views
from models.base_model import BaseModel
from models import storage
from models.state import State
from flask import jsonify, abort
from models import storage
from models import State


@app_views.route('/states', methods=['GET'])
def states(state):
    """ Uses to_dict to retrieve an object into a valid JSON """
    all_states = storage.all('State')
    list = []
    for state in all_states.values():
        list.append(state.to_dict())
    return jsonify(list)


@app_views.route('/states/<state_id>', methods=['GET'])
def individual_states(state_id):
    """ Retrieves a State object, or returns a 404 if the state_id is not
    linked to any object """
    state = storage.get("State", "state_id")
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/state_id', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object, or returns a 404 if the state_id is not
    linked to any object """
    state = storage.get("State", "state_id")
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'])
def create_state():
    """ Creates a State object, or returns a 400 if the HTTP body request is not
    valid JSON, or if the dict doesnt contain the key name """
    if request.method == "POST":
        data = ""
        try:
            data = request.get_json()
        except ValueError:
            abort(400, "Not a JSON")
        name = data.get("name")
        if name is None:
            abort(400, "Missing name")
        new_state = State()
        new_state.name = name
        new_state.save()
        return (jsonify(new_state.to_dict())), 201
