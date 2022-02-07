#!/usr/bin/python3
"""State"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states",
                 methods=["GET"],
                 strict_slashes=False)
def states_all():
    """Retrieves all states with a list of objects"""
    lists = []
    s = storage.all('State').values()
    for v in s:
        lists.append(v.to_dict())
    return jsonify(lists)


@app_views.route("/states/<state_id>",
                 methods=["GET"],
                 strict_slashes=False)
def state_id0(state_id):
    """id state retrieve json object"""
    state_obj = storage.get(State, state_id)
    if state_obj:
        return jsonify(state_obj.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def state_delete(state_id):
    """delete state with id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states',
                 methods=['POST'],
                 strict_slashes=False)
def statePost():
    """Creates a new state"""
    date = request.get_json()
    if date is None:
        return "Not a JSON", 400
    elif "name" not in date.keys():
        return "Missing name", 400
    else:
        nwe_date = State(**date)
        storage.new(nwe_date)
        storage.save()
        current_state = storage.get(State, nwe_date.id)
        return jsonify(current_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def statePut(state_id):
    """Update a State object"""
    state = storage.get("State", state_id)
    x = request.get_json()
    if state:
        if x:
            ignore = ['id', 'created_at', 'updated_at']
            for x, y in x.items():
                if x not in ignore:
                    setattr(state, x, y)
            state.save()
            return jsonify(state.to_dict()), 200
        else:
            return "Not a JSON", 400
    else:
        abort(404)
