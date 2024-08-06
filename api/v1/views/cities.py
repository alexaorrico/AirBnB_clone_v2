#!/usr/bin/python3
"""
This file contains the City module for handling
API actions related to City objects.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from flasgger.utils import swag_from


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get.yml', methods=['GET'])
def get_cities(state_id):
    """
    Retrieve all City objects for a given State.

    This function retrieves all City objects that belong to a specific State
    identified by the state_id.

    Args:
        state_id (str): The ID of the State
        for which cities are to be retrieved.

    Returns:
        Response: JSON response containing a list of all City objects
                  associated with the given State, or a 404 error if the
                  State is not found.
    """
    # Retrieve the State object using the state_id
    state = storage.get(State, state_id)

    # If the State object does not exist, abort with a 404 error
    if state is None:
        abort(404)

    # Create a list of dictionaries for each City object in the State
    list_cities = [obj.to_dict() for obj in state.cities]

    # Return the list of City objects as a JSON response
    return jsonify(list_cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/city/get_id.yml', methods=['GET'])
def get_city(city_id):
    """
    Retrieve a City object by its ID.

    This function retrieves a specific City object using its unique ID.

    Args:
        city_id (str): The ID of the City object to retrieve.

    Returns:
        Response: JSON response containing the City object if found,
                  or a 404 error if not found.
    """
    # Retrieve the City object using its ID
    city = storage.get(City, city_id)

    # If the City object does not exist, abort with a 404 error
    if city is None:
        abort(404)

    # Return the City object as a JSON response
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/city/delete.yml', methods=['DELETE'])
def del_city(city_id):
    """
    Delete a City object by its ID.

    This function deletes a specific City object using its unique ID.

    Args:
        city_id (str): The ID of the City object to delete.

    Returns:
        Response: JSON response with an empty dictionary if the City
                  object was deleted successfully, or a 404 error if not found.
    """
    # Retrieve the City object using its ID
    city = storage.get(City, city_id)

    # If the City object does not exist, abort with a 404 error
    if city is None:
        abort(404)

    # Delete the City object from storage
    city.delete()

    # Save the changes to storage
    storage.save()

    # Return an empty JSON response indicating successful deletion
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/city/post.yml', methods=['POST'])
def create_obj_city(state_id):
    """
    Create a new City object.

    This function creates a new City object based on the provided JSON data,
    associating it with a specific State identified by the state_id.

    Args:
        state_id (str): The ID of the State to which the new City belongs.

    Returns:
        Response: JSON response containing the newly created City object
                  and a status code of 201, or a 400 error if the input
                  is invalid, or a 404 error if the State is not found.
    """
    # Retrieve the State object using the state_id
    state = storage.get(State, state_id)

    # If the State object does not exist, abort with a 404 error
    if state is None:
        abort(404)

    # Check if the request data is valid JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Check if the 'name' field is present in the JSON data
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    # Retrieve the JSON data from the request
    js = request.get_json()

    # Create a new City object using the JSON data
    obj = City(**js)

    # Set the state_id of the City object to associate it with the State
    obj.state_id = state.id

    # Save the new City object to storage
    obj.save()

    # Return the newly created City object as a JSON response
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/city/put.yml', methods=['PUT'])
def post_city(city_id):
    """
    Update an existing City object.

    This function updates a specific City object based on the provided
    JSON data and its unique ID.

    Args:
        city_id (str): The ID of the City object to update.

    Returns:
        Response: JSON response containing the updated City object,
                  or a 400 error if the input is invalid,
                  or a 404 error if the City object is not found.
    """
    # Check if the request data is valid JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Retrieve the City object using its ID
    obj = storage.get(City, city_id)

    # If the City object does not exist, abort with a 404 error
    if obj is None:
        abort(404)

    # Iterate over the JSON data and update the City's attributes
    for key, value in request.get_json().items():
        # Skip updating certain attributes
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    # Save the updated City object to storage
    storage.save()

    # Return the updated City object as a JSON response
    return jsonify(obj.to_dict())
