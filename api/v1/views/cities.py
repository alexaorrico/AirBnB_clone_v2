#!/usr/bin/python3
"""
Create a new view for City objects - handles all default RESTful API actions.
"""

# Import necessary modules
from flask import abort, jsonify, request

# Import the State and City models
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


# Route for retrieving all City objects of a specific State
@app_views.route(
    "/states/<state_id>/cities",
    methods=["GET"],
    strict_slashes=False,
)
def get_cities_by_state(state_id):
    """
    Retrieves all City objects of a specific State.
    """
    # Get the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if state:
        # Get all City objects of the State from the storage
        cities = [city.to_dict() for city in state.cities]
        # Return the City objects in JSON format
        return jsonify(cities)
    else:
        # Return 404 error if the State object is not found
        abort(404)


# Route for retrieving a specific City object by ID
@app_views.route(
    "/cities/<city_id>",
    methods=["GET"],
    strict_slashes=False,
)
def get_city(city_id):
    """
    Retrieves a City object by ID.
    """
    # Get the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if city:
        # Return the City object in JSON format
        return jsonify(city.to_dict())
    else:
        # Return 404 error if the City object is not found
        abort(404)


# Route for deleting a specific City object by ID
@app_views.route(
    "/cities/<city_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_city(city_id):
    """
    Deletes a City object by ID.
    """
    # Get the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if city:
        # Delete the City object from the storage
        storage.delete(city)
        # Save the changes
        storage.save()
        # Return an empty response with 200 status code
        return jsonify({}), 200
    else:
        # Return 404 error if the City object is not found
        abort(404)


# Route for creating a new City object under a specific State
@app_views.route(
    "/states/<state_id>/cities",
    methods=["POST"],
    strict_slashes=False,
)
def create_city(state_id):
    """
    Creates a new City object.
    """
    # Get the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if state:
        # Check if the request data is in JSON format
        if not request.get_json():
            # Return 400 error if the request data is not in JSON format
            abort(400, "Not a JSON")

        # Get the JSON data from the request
        data = request.get_json()
        # Check if the JSON data has the required attribute
        if "name" not in data:
            abort(400, "Missing name")

        # Create a new City object with the JSON data
        city = City(**data)
        # Set the state_id attribute of the City object
        city.state_id = state_id
        # Save the new City object to the storage
        city.save()
        # Return the new City object in JSON format with 201 status code
        return jsonify(city.to_dict()), 201
    else:
        # Return 404 error if the State object is not found
        abort(404)


# Route for updating an existing City object by ID
@app_views.route(
    "/cities/<city_id>",
    methods=["PUT"],
    strict_slashes=False,
)
def update_city(city_id):
    """
    Updates an existing City object by ID.
    """
    # Get the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if city:
        # Check if the request data is in JSON format
        if not request.get_json():
            # Return 400 error if the request data is not in JSON format
            abort(400, "Not a JSON")

        # Get the JSON data from the request
        data = request.get_json()
        # Update the City object with the JSON data
        for key, value in data.items():
            if key not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, key, value)
        # Save the updated City object to the storage
        city.save()
        # Return the updated City object in JSON format with 200 status code
        return jsonify(city.to_dict()), 200
    else:
        # Return 404 error if the City object is not found
        abort(404)
