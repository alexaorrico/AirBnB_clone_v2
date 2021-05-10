#!/usr/bin/python3
"""Config endpoint for REST resource states"""
from flask import Flask, abort, jsonify, make_response
from flask import request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=["POST", "GET"])
@app_views.route('/states/<state_id>', methods=('DELETE', 'PUT', "GET"))
def states_get_id(state_id=None):
    """Retrieves a state object by its id"""

    states_dict = storage.all(State)
    obj_list = []

    if state_id is not None:
        my_state_obj = storage.get(State, state_id)

        if my_state_obj is not None:
            if request.method == 'DELETE':
                storage.delete(my_state_obj)
                return make_response(jsonify({}), 200)

            if request.method == 'GET':
                return jsonify(my_state_obj.to_dict())

            if request.method == 'PUT':
                update_dict = request.get_json(silent=True)
                if update_dict is not None:
                    for key, value in update_dict.items():
                        setattr(my_state_obj, key, value)
                        my_state_obj.save()
                    return make_response(jsonify(my_state_obj.to_dict()), 200)
                else:
                    abort(400, "Not a JSON")
        else:
            abort(404)
    else:
        # In case state_id is None
        if request.method == 'POST':
            my_json = request.get_json(silent=True)
            if my_json is not None:
                if "name" in my_json:
                    name = my_json["name"]
                    new_state = State(name=name)
                    new_state.save()
                    return make_response(jsonify(new_state.to_dict()), 201)
                else:
                    abort(400, "Missing name")
            else:
                # print("funcionó el none!")
                abort(400, "Not a JSON")

        for value in states_dict.values():
            obj_list.append(value.to_dict())
        return jsonify(obj_list)
