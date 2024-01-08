"""
Module containing Flask routes for handling State resources.
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """
    Handles GET and POST requests for the /states route.

    GET: Retrieves a list of all states.
    POST: Creates a new state.

    Returns:
        JSON response containing a list of states or the newly created state.
    """
    if request.method == 'GET':
        # Retrieve all states
        states = storage.all("State")
        states_list = []
        for value in states.values():
            states_list.append(value.to_dict())
        return jsonify(states_list)

    elif request.method == 'POST':
        try:
            # Attempt to get JSON data from the request
            state_json = request.get_json()
        except Exception as e:
            return f"Not a JSON", 400

        if "name" not in state_json:
            abort(400, description="Missing name")

        new_state = State(**state_json)
        storage.new(new_state)
        storage.save()

        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def state(state_id):
    """
    Handles GET, DELETE, and PUT requests for a specific state
    identified by state_id.

    GET: Retrieves information about a specific state.
    DELETE: Deletes a specific state.
    PUT: Updates information about a specific state.

    Args:
        state_id (str): The ID of the state.

    Returns:
        JSON response containing state information, an empty dictionary,
        or updated state information.
    """
    if request.method == 'GET':
        # Retrieve and delete a specific state from storage
        state = storage.get("State", state_id)
        if not state:
            abort(404)

        return jsonify(state.to_dict())

    elif request.method == 'DELETE':
        state = storage.get("State", state_id)
        if state is None:
            abort(404)

        storage.delete(state)
        storage.save()
        return {}

    elif request.method == 'PUT':
        # Retrieve a specific state from storage by state_id
        state = storage.get("State", state_id)
        if state is None:
            abort(404)

        try:
            state_json = request.get_json()
        except Exception as e:
            return f"Not a JSON", 400

        state.name = state_json['name']
        state.save()

        return jsonify(state.to_dict()), 200
