#!/usr/bin/python3

"""
create new view for City objects
that handles all default RESTFul API actions
    - retrive a list of City object by state id
    - retrive a City object
    - delete a City object
    - create a new City object
    - update a City object
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def city_by_state(state_id):
    """
    Retrieves the list of all City objects of a State
    using the state id
    """
    if state_id is not None:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        cityList = [city.to_dict() for city in state.cities]
        return jsonify(cityList)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    """
    Retrieves a City object by the id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object by the id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a city using state_id
    """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        new_city = City()
        new_city.state_id = state_id
        new_city.name = request.get_json().get('name')
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    update a city object
    """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.name = request.get_json().get('name')
    city.save()
    return jsonify(city.to_dict())
