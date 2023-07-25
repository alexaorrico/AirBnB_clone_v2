#!/usr/bin/python3
""" create a new view for City objects that
    handle all default RESTFul API actions """
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request
from models.state import State
from models.city import City


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_states_cities(state_id):
    """ retrives city objects of states """
    the_state = storage.get(State, state_id)
    if not the_state:
        abort(404)
    cities_list = []
    for city in the_state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ retrive a city object """
    the_city = storage.get(City, city_id)
    if not the_city:
        abort(404)
    return jsonify(the_city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ deletes a city object """
    the_city = storage.get(City, city_id)
    if not the_city:
        abort(404)
    storage.delete(the_city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Create a city object """
    data = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    elif not data:
        abort(400, "Not a JSON")
    elif "name" not in data:
        abort(400, "Missing name")
    data["state_id"] = state_id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ updates a city """
    data = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    elif not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
