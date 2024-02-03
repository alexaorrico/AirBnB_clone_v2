#!/usr/bin/python3
""" module to get views of object state"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from flask import abort
from flask import request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id=None):
    """ get list of all states or one state based on state_id"""
    _lst = []
    states = storage.all(State).values()
    for state in states:
        if state_id is not None and state.id != state_id:
            continue
        _lst.append(state.to_dict())
        if state_id and state.id == state_id:
            break
    if state_id:
        if not _lst:
            abort(404)
        else:
            return jsonify(_lst[0])
    return jsonify(_lst)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_state(state_id=None):
    """ delete object based on state_id"""
    ref_state_obj = storage.get(State, state_id)
    if ref_state_obj is None:
        abort(404)
    storage.delete(ref_state_obj)
    # commit the  delete action
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ create new State """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    obj_state = State(**data)
    obj_state.save()
    return jsonify(obj_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ update state based on state_id"""
    ref_obj_state = storage.get(State, state_id)
    if not ref_obj_state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key in data:
        if key not in ['id', 'created_at', 'updated_at']:
            # ref_obj_state.__dict__[key] = data[key]
            setattr(ref_obj_state, key, data[key])
    storage.save()
    return jsonify(ref_obj_state.to_dict()), 200
