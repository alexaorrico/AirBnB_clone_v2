#!/usr/bin/python3
"""
view for State objects that handles all default RestFul API actions
"""

from flask import jsonify, request, abort, make_response
from models import storage
# we import the Blueprint 'app_views'created in the __init__
from api.v1.views import app_views
from models.state import State


# the followings are the entendpoints of the app_view blueprint
# in other words /status == /api/v1/status and /stats == /api/v1/stats
# we create that blueprint to access to all the endpoints easily

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """
    function to return the all State objects
    """
    all_states = []
    for item in storage.all('State').values():
        all_states.append(item.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """
    function to return State object by id throught a GET method
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404, description="state_id not linked to any State object")
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    function to delete State object by id throught a DELETE method
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404, description="state_id not linked to any State object")
    state.delete()
    storage.save()
    response = make_response(jsonify({}), 200)
    return response


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """
    function to create a new State object throught a POST method
    """
    dic_json = request.get_json()
    if not dic_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in dic_json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = State(**dic_json)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    function to update a State object by id throught a PUT method
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404, description="state_id not linked to any State object")
    dic_json = request.get_json()
    if not dic_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in dic_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
