#!/usr/bin/python3
""" CRUD operation on city object"""
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import abort, request, make_response


@app_views.route('/states/<id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(id):
    """
    The function `get_cities_by_state` retrieves a list of
    cities belonging to a specific state and returns them
    as a JSON response.
    """
    state = storage.get(State, id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<id>', methods=['GET'], strict_slashes=False)
def city_id(id):
    """
    The function retrieves a city object from storage based
    on its ID and returns its dictionary representation as
    a JSON response, or returns a 404 error if the city is
    not found.
    """
    city = storage.get(City, id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<id>', methods=['DELETE'], strict_slashes=False)
def city_id_delete(id):
    """
    The function `city_id_delete` deletes a city
    object from storage based on its ID.
    """
    city = storage.get(City, id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(id):
    """
    The function `city_post()` receives a JSON object,
    checks if it is valid, creates a new city object,
    saves it to storage, and returns the city object as a JSON response.
    """
    state = storage.get(State, id)
    if not state:
        abort(404)
    if not request.get_json():
        make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'name' not in data or data['name'] == "":
        make_response(jsonify({"error": "Missing name"}), 400)
    data['state_id'] = id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('cities/<id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    """
    The function updates the attributes of a city object based
    on the provided JSON data and returns the updated state
    object as a JSON response."""
    city = storage.get(City, id)
    if city:
        if not request.get_json():
            make_response(jsonify({"error": "Not a JSON"}), 400)
        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)
