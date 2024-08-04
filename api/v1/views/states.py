#!/usr/bin/python3
"""
router for states
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """
    GET state objects
    :return: list of states in JSON format
    """
    list_states = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        list_states.append(obj.to_json())

    return jsonify(list_states)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    POST to create a new state
    :return: JSON string of the new state
    """
    state_string = request.get_json(silent=True)
    if state_string is None:
        abort(400, 'Not a JSON')
    if "name" not in state_string:
        abort(400, 'Missing name')

    new_state = State(**state_string)
    new_state.save()
    resp = jsonify(new_state.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def access_state_by_id(state_id):
    """
    get state id
    :param state_id: state id
    :return: state id in JSON
    """
    get_obj = storage.get("State", str(state_id))

    if get_obj is None:
        abort(404)

    return jsonify(get_obj.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    updates state by id
    :param state_id: state object ID
    :return: new state in JSON
    """
    state_string = request.get_json(silent=True)
    if state_string is None:
        abort(400, 'Not a JSON')
    get_obj = storage.get("State", str(state_id))
    if fetched_obj is None:
        abort(404)
    for key, val in state_string.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(get_obj, key, val)
    get_obj.save()
    return jsonify(getd_obj.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    delete a state by id
    :param state_id: state id
    :return: empty string showing deletion
    """
    get_obj = storage.get("State", str(state_id))

    if get_obj is None:
        abort(404)

    storage.delete(get_obj)
    storage.save()

    return jsonify({})
