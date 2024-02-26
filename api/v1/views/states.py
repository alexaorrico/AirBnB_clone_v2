#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """Retrieves the list of all State objects"""
    list_of_states = []
    objects = storage.all("State")
    for obj in objects.values():
        list_of_states.append(obj.to_dict())
    return jsonify(list_of_states)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """Creates a State: POST /api/v1/states"""
    json_sts = request.get_json(silent=True)
    if json_sts is None:
        abort(400, 'Not a JSON')
    if "name" not in json_sts:
        abort(400, 'Missing name')
    new_s = State(**json_sts)
    new_s.save()
    response = jsonify(new_s.to_dict())
    response.status_code = 201
    return response


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """get a state with aspecific id
    Args:
        state_id: state id"""
    obj = storage.get("State", str(state_id))
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """update a state with the id passed
    Args:
        state_id: state id"""
    sts_json = request.get_json(silent=True)
    if sts_json is None:
        abort(400, "Not a JSON")
    obj = storage.get("State", str(state_id))
    if obj is None:
        abort(404)
    for k, v in sts_json.items():
        if k not in ["id", "create_at", "update_at"]:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """Delete a state with a specific if
    Args:
        state_id: state id"""
    obj = storage.get("State", str(state_id))
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})
