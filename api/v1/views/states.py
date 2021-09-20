#!/usr/bin/python3
"""
script that starts a Flask web application:
"""

from models import storage
from api.v1.views import app_views
from flask import abort
from flask import jsonify, request
from models import storage, state


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def state_all():
    """
    Retrieves the list of all State objects
    """
    list = []
    for state in storage.all("State").values():
        list.append(state.to_dict())
    return jsonify(list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_get(state_id):
    """
    Retrieves a State object:
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id=None):
    """
    Deletes a State object
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json().keys():
        abort(400, "Missing name")
    else:
        my_state = state.State(**request.get_json())
        storage.new(my_state)
        storage.save()
        resp = my_state.to_dict()
        return jsonify(resp), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id=None):
    """
    Updates a State object
    """
    states = storage.get("State", state_id)
    if states is None:
        abort(404)
    st = request.get_json()
    if st is None:
        abort(400, "Not a JSON")
    else:
        for key, value in st.items():
            if key in ['id'] and key in ['created_at']\
                    and key in ['updated_at']:
                pass
            else:
                setattr(states, key, value)
        storage.save()
        resp = states.to_dict()
        return jsonify(resp), 200
