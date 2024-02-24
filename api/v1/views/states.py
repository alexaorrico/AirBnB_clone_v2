#!/usr/bin/python3
"""
States view
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def get_state():
    """ Gets a single state
    """
    state_list = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        state_list.append(obj.to_dict())

    return jsonify(state_list)


@app_views.route("/states/<string:state_id>", methods=["GET"],
                 strict_slashes=False)
def get_states(state_id):
    """ Gets state based on id passed"""
    state_obj = storage.get("State", 'state_id')
    if state_obj is None:
        abort(404)

    return jsonify(state_obj.to_dict())


@app_views.route("/states/<string:state_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_state(state_id):
    """ Deletes a state using ID"""
    state_obj = storage.get('State', "state_id")
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), '200'


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def create_state():
    """Create a new post"""
    new_state = request.get_json()
    if new_state is None:
        abort(400, "Not a JSON")

    if "name" is None:
        abort(400, "Missing name")

    state_instance = State(**new_state)
    storage.new(state_instance)
    storage.save()
    resp = jsonify(state_instance.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/states/<string:state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_states(state_id):
    """Updates an existing state"""
    state_obj = storage.get("State", "state_id")
    if state_obj is None:
        abort(404)

    new_state = request.get_json()
    if new_state is None:
        abort(400, "Not a JSON")

    ignoreKeys = ['id', 'created_at', 'updated_at']
    for key in new_state.items():
        if key not in ignoreKeys:
            setattr(state_obj, key)
    storage.save()
    return jsonify(state_obj.to_dict()), '200'
