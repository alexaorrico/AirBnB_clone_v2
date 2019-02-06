#!/usr/bin/python3
"""view of State object"""
from api.v1.views import app_views
from models import storage, state
from flask import jsonify, abort, request


@app_views.route('/states', methods=["GET"])
def states_ret():
    """return json State objects"""
    state_list = []
    all_objs = storage.all("State")
    for obj in all_objs.values():
        state_list.append(obj.to_dict())
    return jsonify(state_list)

@app_views.route('/states/<state_id>', methods=["GET"])
def get_by_id(state_id):
    """return json State objects by id"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/states', methods=["DELETE"])
@app_views.route('/states/<state_id>', methods=["DELETE"])
def state_delete(state_id=None):
    """delete an object by id"""
    if state_id is None:
        abort(404)
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/', methods=["POST"])
def post_obj():
    """add new state object"""
    dic = {}
    try:
        dic = request.get_json()
    except:
        abort(400, "Not a JSON")
    if "name" not in dic.keys():
        abort(400, "Missing name")
    else:
        new_state = state.State()
        for k, v in dic.items():
            setattr(new_state, k, v)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states', methods=["PUT"])
@app_views.route('/states/<state_id>', methods=["PUT"])
def update_obj(state_id=None):
    """update new state object"""
    dic = {}
    ignore_key = ["id", "created_at", "updated_at"]
    if state_id is None:
        abort(404)
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    try:
        dic = request.get_json()
    except:
        abort(400, "Not a JSON")
    for key, value in dic.items():
        if key not in ignore_key:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
