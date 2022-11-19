#!/usr/bin/python3
"""
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, state

state_list = [obj.to_dict() for obj in storage.all(state.State).values()]
@app_views.route("/states", strict_slashes=False, defaults={'state_id': None}, methods=['GET', 'POST', 'PUT'])
@app_views.route("/states/<state_id>",  methods=['GET', 'POST', 'DELETE', 'PUT'])
def get_state(state_id):
    if request.method == "GET":
        if state_id is None:
            return state_list
        elif state_id is not None:
            for obj in state_list:
                if obj.get("id") == state_id:
                    return obj
        abort(404)
    elif request.method == "POST":
        try:
            post_data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)
        if 'name' not in post_data:
            return make_response("Missing name", 400)
        new_state = state.State()
        new_state.name = post_data['name']
        new_state.save()
        return make_response(new_state.to_dict(), 201)
    elif request.method == "PUT":
        try:
            put_data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)
        for obj in state_list:
            if obj.get("id") == state_id:
                for key, value in put_data.items():
                    obj[key] = value
                obj.save()
                return make_response(obj, 200)
        abort(404)
    elif request.method == "DELETE":
        state_obj = storage.get("State", state_id)
        if state_obj is None:
            abort(404)
        state_obj.delete()
        storage.save()
        return (jsonify({}))
