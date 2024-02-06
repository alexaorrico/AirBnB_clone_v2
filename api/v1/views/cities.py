#!/usr/bin/python3
"""Module to handle rest api actions to city"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """method to get all cities in a given state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    # making use of SQLAchemy ORM backref pointing states to its
    # corresponding cities
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """method to get a city by id"""
    for city in storage.all(City).values():
        if city.id == city_id:
            return jsonify(city.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """method to delete city"""
    for city in storage.all(City).values():
        if city.id == city_id:
            # storage.delete(city)
            city.delete()
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """method to create new city under a given state"""
    valid_state = False
    for state in storage.all(State).values():
        if state.id == state_id:
            valid_state = True
    if not valid_state:
        abort(404)

    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, "Not a JSON")
    if 'name' not in request_data:
        abort(400, "Missing name")

    request_data["state_id"] = state_id
    kwargs = {attrib: value for attrib,
              value in request_data.items() if attrib in ["name", "state_id"]}
    new_city = City(**kwargs)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """method to update city"""
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, "Not a JSON")
    for city in storage.all(City).values():
        if city.id == city_id:
            for attrib, value in request_data.items():
                if attrib in ['id', 'state_id', 'created_at', 'updated_at']:
                    continue
                setattr(city, attrib, value)
            city.save()
            return make_response(jsonify(city.to_dict()), 200)
    abort(404)
