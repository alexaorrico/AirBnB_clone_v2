#!/usr/bin/python3
""" Module for storing indeces for the route to states. """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def return_list_all_cities_by_state(state_id):
    """ Returns cities by state id. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = state.cities
    list_of_json_cities = []
    for city in list_cities:
        list_of_json_cities.append(city.to_dict())
    return(jsonify(list_of_json_cities))


@app_views.route("/cities/<city_id>", methods=["GET"])
def return_city_by_id(city_id):
    """ Returns city by id. """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return(jsonify(city.to_dict()))


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city_obj(city_id):
    """ Deletes a city object by id. """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return({})
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city_obj(state_id):
    """ Creates a new City linked to a State.  """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data.keys():
        abort(400, "Missing name")
    if storage.get(State, state_id) is None:
        abort(404)
    data["state_id"] = state_id
    city = City(**data)
    city.save()
    return(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city_obj(city_id):
    """ Updates a city by its id. """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignored_keys = ["id", "state_id", "created_at", "updated_at"]
    city = storage.get(City, city_id)
    if city:
        for key, value in data.items():
            if key not in ignored_keys:
                setattr(city, key, value)
            city.save()
        return(jsonify(city.to_dict()))
    abort(404)
