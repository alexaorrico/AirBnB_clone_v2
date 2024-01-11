#!/usr/bin/python3
"""City view objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, app, jsonify, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities(state_id):
    """Retrieves the list of all City objects of a State
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city(city_id):
    """Retrieves a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return city.to_dict()


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return {}, 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city = request.get_json()
    if city is None:
        abort(400, "Not a JSON")
    if "name" not in city:
        abort(400, "Missing name")
    city = City(**city)
    city.state_id = state_id
    city.save()
    return city.to_dict(), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city_data = request.get_json()
    if city_data is None:
        abort(400, "Not a JSON")
    for key, value in city_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return city.to_dict(), 200
