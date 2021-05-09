#!/usr/bin/python3
"""states route handler"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


def check(id):
    """
        checking if state is valid in storage
    """
    try:
        checker = storage.get(State, id)
        checker.to_dict()
    except Exception:
        abort(404)
    return checker


def get_all(id_state):
    """
        getting all states from storage
    """
    if id_state is not None:
        state = check(id_state)
        dict_state = state.to_dict()
        return jsonify(dict_state)
    states = storage.all(State)
    states_all = []
    for x in states.values():
        states_all.append(x.to_dict())
    return jsonify(states_all)


def delete_state(id_state):
    """
        deleting a state request
    """
    state = check(id_state)
    storage.delete(state)
    storage.save()
    response = {}
    return jsonify(response)


def create_state(request):
    """
        Create new state request
    """
    request_json = request.get_json()
    if request_json is None:
        abort(400, 'Not a JSON')
    try:
        name_state = request_json['name']
    except Exception:
        abort(400, "Missing name")
    state = State(name=name_state)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict())


def update_state(state_id, request):
    """
        Update state if found
    """
    state = check(state_id)
    request_json = request.get_json()
    if request_json is None:
        abort(400, 'Not a JSON')
    for x, y in request_json.items():
        if (x not in ('id', 'created_at', 'updated_at')):
            setattr(state, x, y)
        storage.save()
        return jsonify(state.to_dict())


@app_views.route('/states/', methods=['GET', 'POST'],
                 defaults={'state_id': None}, strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'])
def states(state_id):
    """
    Global Method to handle request
    """
    if (request.method == "GET"):
        return get_all(state_id)
    elif request.method == "DELETE":
        return delete_state(state_id)
    elif request.method == "POST":
        return create_state(request), 201
    elif request.method == 'PUT':
        return update_state(state_id, request), 200
