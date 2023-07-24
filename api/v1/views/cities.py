#!/usr/bin/python3
""" create a new view for City objects that
    handle all default RESTFul API actions """
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request
from models.state import State
from models.city import City


@app_views.route('states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_states_cities(state_id):
    """ retrives city objects of states """
    the_state = storage.get(State, state_id)
    cities_list = []
    if the_state is None:
        abort(404)
    for city in the_state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ retrive a city object """
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    return jsonify(the_city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ deletes a city object """
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    storage.delete(the_city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Create a city object """
    state = storage.get(State, state_id)
    data = request.get_json()
    if state is None:
        abort(404)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data.keys():
        return jsonify({"error": "Missing name"}), 400
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<string:city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ updates a city """
    city = storage.get(City, city_id)
    data = request.get_json()
    if city is None:
        abort(404)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
