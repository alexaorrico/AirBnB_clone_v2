#!/usr/bin/python3
"""
The following script creates a new City objects view
and handles all default RESTful API actions.
"""


# Importing necessary modules
from flask import abort, jsonify, request
# Importing the State and City models
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """
    The method retrieves the list of all the City objects of a State

    Args:
        state_id (str): The ID of the State.

    Returns:
        JSON: List of all City objects in JSON format.
    Raises:
        404: If the State object with the given ID is not found.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    This method retrieves a City object

    Args:
        city_id (str): The ID of the City.

    Returns:
        JSON: City object in JSON format.
    Raises:
        404: If the City object with the given ID is not found.
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    This method deletes a City object

    Args:
        city_id (str): The ID of the City.

    Returns:
        JSON: Empty JSON with a status code of 200.
    Raises:
        404: If the City object with the given ID is not found.
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    The methodcreates a City object.

    Args:
        state_id (str): The ID of the State.

    Returns:
        JSON: Newly created City object in JSON format with status code of 201
    Raises:
        404: If the State object with the given ID is not found
        400: If the request data isnt in JSON format or if namekey is missing
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    The following method updates a City object.

    Args:
        city_id (str): The ID of the City.

    Returns:
        JSON: Updated City object in JSON format with a status code of 200.
    Raises:
        404: If the City object with the given ID is not found.
        400: If the request data is not in JSON format.
    """
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)

        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """
    The method returns:
        JSON: Error response for 404 status code.
    """
    return jsonify({'error': 'Not found'}), 404


@app_views.errorhandler(400)
def bad_request(error):
    """
    The methodReturns Bad Request message for illegal requests to API

    Returns:
        JSON: Error response for 400 status code.
    """
    return jsonify({'error': 'Bad Request'}), 400
