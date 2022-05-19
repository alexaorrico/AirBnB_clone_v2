#!/usr/bin/python3
import json
from models import storage
from flask import jsonify, abort, request, make_response
from models.state import State
from api.v1.views import app_views

@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states():
    """ Retrieves the list of all State objects """
    list_states = []
    states = storage.all(State).values()
    for state in states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route("/states/<state_id>", methods=['GET', 'DELETE'], strict_slashes=False)
def states_id(state_id):
    """ Retrieves a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    elif request.method == 'DELETE':
        storage.delete(state)
        del state
        storage.save()
        return jsonify({})
