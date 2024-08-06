#!/usr/bin/python3


"""  TODO: Doc """


from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage


states_dicts = storage.all(State)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    array_of_objs = []
    for value in states_dicts.values():
        array_of_objs.append(value.to_dict())
    return jsonify(array_of_objs)


"""
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def StateById(state_id):
    state_obj = storage.get(State, state_id)
    if f"State.{state_id}" not in states_dicts or not state_obj:
        abort(404, description="State not found")
    else:
        if request.method == 'GET':
            return jsonify(state_obj.to_dict())
        elif request.method == 'DELETE':
            try:
                storage.delete(state_obj)
                storage.save()
                return jsonify({}), 200
            except Exception:
                abort(404, description="error while deleting")
        elif request.method == 'PUT':
            if request.is_json:
                data = request.get_json()
                bad_keys = ['id', 'created_at', 'updated_at']
                for key in data.keys():
                    if key not in bad_keys:
                        setattr(state_obj, key, data[key])
                return jsonify(state_obj.to_dict()), 200
            else:
                abort(400, description="Not a JSON")
"""


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_ById(state_id):
    """  TODO: Doc """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404, description="State not found")
    return jsonify(state_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """  TODO: Doc """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404, description="State not found")
    try:
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(500, description="Error while deleting")


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """  TODO: Doc """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404, description="State not found")
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    bad_keys = ['id', 'created_at', 'updated_at']
    for key in data.keys():
        if key not in bad_keys:
            setattr(state_obj, key, data[key])
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """  TODO: Doc """
    if request.is_json:
        data = request.get_json()
        if 'name' not in data:
            abort(400, description="Missing name")
        else:
            state_obj = State(**data)  # unpack dict as key:valus
            state_obj.save()
            return jsonify(state_obj.to_dict()), 201
    else:
        abort(400, description="Not a JSON")
