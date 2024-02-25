#!/usr/bin/python3
"""
Create a new view for State objects - handles all default RESTful API actions.
"""

# Import necessary modules
from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage


# Route for retrieving all State objects
@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """
    Retrieves the list of all State objects.
    """
    # Get the list of all State objects from the storage
    states = storage.all(State).values()
    # Convert the list of State objects to a dictionary
    states = [state.to_dict() for state in states]
    # Return the list of State objects in JSON format
    return jsonify(states)


# Route for retrieving a specific State object by ID
@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object by ID.
    """
    # Get the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if not state:
        # Return 404 error if the State object is not found
        abort(404)
    # Return the State object in JSON format
    return jsonify(state.to_dict())


# Route for deleting a specific State object by ID
@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """
    Deletes a State object by ID.
    """
    # Get the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if not state:
        # Return 404 error if the State object is not found
        abort(404)
    # Delete the State object from the storage
    state.delete()
    # Return an empty dictionary with 200 status code
    return jsonify({}), 200


# Route for creating a new State object
@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Creates a new State object.
    """
    if not request.get_json():
        # Return 400 error if the request data is not in JSON format
        abort(400, "Not a JSON")

    # Get the JSON data from the request
    data = request.get_json()
    if "name" not in data:
        # Return 400 error if the request data does not contain the key 'name'
        abort(400, "Missing name")

    # Create a new State object with the JSON data
    state = State(**data)
    # Save the new State object to the storage
    state.save()
    # Return the new State object in JSON format with 201 status code
    return jsonify(state.to_dict()), 201


# Route for updating an existing State object by ID
@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object by ID.
    """
    # Get the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if not state:
        # Return 404 error if the State object is not found
        abort(404)

    if not request.get_json():
        # Return 400 error if the request data is not in JSON format
        abort(400, "Not a JSON")

    # Get the JSON data from the request
    data = request.get_json()
    # Update the State object and save the changes
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    # Return the State object in JSON format with 200 status code
    return jsonify(state.to_dict()), 200


@app_views.errorhandler(404)
def not_found(error):
    """
    Returns a Not Found message for requests to the API with invalid ID.
    """
    # Return a JSON response for 404 error
    response = {"error": error.description}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """
    Returns a Bad Request message for requests to the API with invalid data.
    """
    # Return a JSON response for 400 error
    response = {"error": error.description}
    return jsonify(response), 400
