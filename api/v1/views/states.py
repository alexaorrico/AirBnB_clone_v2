#!/usr/bin/python3
"""Flask module to configure routes for state class api calls"""
from models.state import State
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route("/states",
                 defaults={"state_id": None},
                 strict_slashes=False,
                 methods=['GET'])
@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def state_get(state_id):
    """Handle GET request for states"""
    if state_id is None:
        return jsonify(
            [state.to_dict() for state in storage.all("State").values()]
        )
    elif "State" + '.' + state_id in storage.all("State").keys():
        return jsonify(
            storage.get("State", state_id).to_dict()
        )
    else:
        abort(404)


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def state_delete(state_id):
    """Handles DELETE request with state objects"""
    if "State" + '.' + state_id in storage.all("State").keys():
        storage.delete(storage.all("State")['State' + '.' + state_id])
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def state_post():
    """Handles POST request with state objects"""
    try:
        new_state = State(**(request.get_json()))
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    except TypeError:
        abort(404, 'Not a json')
    except KeyError:
        abort(404, 'Missing name')
