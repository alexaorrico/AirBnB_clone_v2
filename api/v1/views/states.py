#!/usr/bin/python3
"""
view for State objects that handles all default RestFul API action
"""

from flask import jsonify, request, abort, make_response
from models import storage
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
def get_state(state_id):
    """
    function to return State object by id throught a GET method
    """
    all_states = storage.all("State").values()
    for state in all_states:
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    function to delete State object by id throught a DELETE method
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
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
        return make_response("Not a JSON", 400)
    if "name" not in dic_json:
        return make_response("Missing name", 400)
    new_state = State(**dic_json)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    function to update a State object by id throught a PUT method
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    dic_json = request.get_json()
    if not dic_json:
        return make_response("Not a JSON", 400)
    for key, value in dic_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)


if __name__ == "__main__":
    pass
