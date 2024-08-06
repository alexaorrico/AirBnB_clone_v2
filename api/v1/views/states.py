#!/usr/bin/python3
"""State module for handling API actions related to State objects."""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get.yml', methods=['GET'])
def get_all():
    """
    Retrieve all State objects.

    This function retrieves all State objects from storage and returns
    them as a JSON response.

    Returns:
        Response: JSON response containing a list of all State objects.
    """
    # Retrieve all State objects and convert them to a list of dictionaries
    all_list = [obj.to_dict() for obj in storage.all(State).values()]

    # Return the list of State objects as a JSON response
    return jsonify(all_list)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/state/get_id.yml', methods=['GET'])
def get_method_state(state_id):
    """
    Retrieve a State object by its ID.

    This function retrieves a specific State object using its unique ID.

    Args:
        state_id (str): The ID of the State object to retrieve.

    Returns:
        Response: JSON response containing the State object if found,
                  or a 404 error if not found.
    """
    # Retrieve the State object using its ID
    state = storage.get(State, state_id)

    # If the State object does not exist, abort with a 404 error
    if state is None:
        abort(404)

    # Return the State object as a JSON response
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete.yml', methods=['DELETE'])
def del_method(state_id):
    """
    Delete a State object by its ID.

    This function deletes a specific State object using its unique ID.

    Args:
        state_id (str): The ID of the State object to delete.

    Returns:
        Response: JSON response with an empty dictionary if the State
                  object was deleted successfully, or a 404 error if not found.
    """
    # Retrieve the State object using its ID
    state = storage.get(State, state_id)

    # If the State object does not exist, abort with a 404 error
    if state is None:
        abort(404)

    # Delete the State object from storage
    state.delete()

    # Save the changes to storage
    storage.save()

    # Return an empty JSON response indicating successful deletion
    return jsonify({})


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post.yml', methods=['POST'])
def create_obj():
    """
    Create a new State object.

    This function creates a new State object based on the provided JSON data.

    Returns:
        Response: JSON response containing the newly created State object
                  and a status code of 201, or a 400 error if the input
                  is invalid.
    """
    # Check if the request data is valid JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Check if the 'name' field is present in the JSON data
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    # Retrieve the JSON data from the request
    js = request.get_json()

    # Create a new State object using the JSON data
    obj = State(**js)

    # Save the new State object to storage
    obj.save()

    # Return the newly created State object as a JSON response
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/state/put.yml', methods=['PUT'])
def post_method(state_id):
    """
    Update an existing State object.

    This function updates a specific State object based on the provided
    JSON data and its unique ID.

    Args:
        state_id (str): The ID of the State object to update.

    Returns:
        Response: JSON response containing the updated State object,
                  or a 400 error if the input is invalid,
                  or a 404 error if the State object is not found.
    """
    # Check if the request data is valid JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Retrieve the State object using its ID
    obj = storage.get(State, state_id)

    # If the State object does not exist, abort with a 404 error
    if obj is None:
        abort(404)

    # Iterate over the JSON data and update the State object's attributes
    for key, value in request.get_json().items():
        # Skip updating certain attributes
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    # Save the updated State object to storage
    storage.save()

    # Return the updated State object as a JSON response
    return jsonify(obj.to_dict())
