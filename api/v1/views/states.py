#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    states_all = storage.all("State")
    states_list = []
    for key, state in states_all.items():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'], strict_slashes=False)
def get_states_id(state_id):
    if request.method == 'GET':
        states_all = storage.all("State")
        try:
            unique_state = states_all["{}.{}".format("State", state_id)].to_dict()
        except KeyError:
            abort(404)
        return jsonify(unique_state)
    elif request.method == 'DELETE':
        obj_to_delete = storage.get("State", state_id)
        if obj_to_delete is None:
            abort(404)
        else:
            storage.delete(obj_to_delete)
            storage.save()
            return jsonify({}), 200
