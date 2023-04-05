#!/usr/bin/python3
"""Flask route module for states"""
from api.v1.views import app_views, validate_model, get_json
from flask import jsonify
from models import storage, class_dictionary


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_no_id_get():
    """states route handling - no id given GET scenario"""
    all_states = storage.all("State")
    all_states = list(obj.to_dict() for obj in all_states.values())
    return jsonify(all_states)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def states_no_id_post():
    """states route handling - no id given POST scenario"""
    req_json = get_json(['name'])
    State = class_dictionary.get("State")
    new_object = State(**req_json)
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_with_id_get(state_id=None):
    """states route handling - id given GET scenario"""
    state_obj = validate_model("State", state_id)
    return jsonify(state_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def states_with_id_del(state_id=None):
    """states route handling - id given DELETE scenario"""
    state_obj = validate_model("State", state_id)
    state_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def states_with_id_put(state_id=None):
    """states route handling - id given PUT scenario"""
    state_obj = validate_model("State", state_id)
    req_json = get_json()
    for key, value in req_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, value)
    state_obj.save()
    return jsonify(state_obj.to_dict())
