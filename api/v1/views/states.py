#!/usr/bin/python3
""" handles all default RESTFul API actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_all():
    """Retrieves the list of all State objects """
    state_l = []
    state_o = storage.all("State")
    for obj in state_o.values():
        state_l.append(obj.to_dict())

    return jsonify(state_l)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete(state_id):
    """Deletes a State object"""
    d_obj = storage.get("State", str(state_id))
    if d_obj is None:
        abort(404)

    storage.delete(d_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """Creates a State"""
    state_j = request.get_json(silent=True)
    if state_j is None:
        abort(400, description='Not a JSON')
    if "name" not in state_j:
        abort(400, description='Missing name')

    new_state = State(**state_j)
    new_state.save()
    repo = jsonify(new_state.to_dict())
    repo.status_code = 201

    return repo


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_update(state_id):
    """update a state"""
    state_j = request.get_json(silent=True)
    if state_j is None:
        abort(400, 'Not a JSON')
    d_obj = storage.get("State", str(state_id))
    if d_obj is None:
        abort(404)
    for key, val in state_j.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(d_obj, key, val)
    d_obj.save()
    return jsonify(d_obj.to_dict())
