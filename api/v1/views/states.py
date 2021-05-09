#!/usr/bin/python3
"""states route handler"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

def check(id):
    """
    """
    try:
        checker = storage.get(State, id)
    except Exception:
        abort(404)
    return checker


def get_all(id_state):
    """
    """
    if id_state is not None:
        state =  check(id_state)
        dict_state = state.to_dict()
        return jsonify(dict_state)
    states = storage.all(State)
    states_all = []
    for x in states.values():
        states_all.append(x.to_dict())
    return jsonify(states_all)

@app_views.route('/states/', methods=['GET', 'POST'],
                 defaults={'state_id': None}, strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'])
def states(state_id):
    """
    """
    if (request.method == "GET"):
        return get_all(state_id)
# add the other method kif maamalt ana