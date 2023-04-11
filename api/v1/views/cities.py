#!/usr/bin/python3
""" handles all default RESTFul API actions for City """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """ retrieves the list of all City object of a specific State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        cities_list = []
        for city in state.cities:
            cities_list.append(city.to_dict())
    return (jsonify(cities_list))


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ retrieves a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        city_id = city.to_dict()
        return (jsonify(city_id))


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ deletes a City object with its id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ creates a City object """
    state = storage.get(State, state_id)
    json_data = request.get_json()
    if state is None:
        abort(404)
    if not json_data:
        abort(400, description="Not a JSON")
    if 'name' not in json_data:
        abort(400, description="Missing name")
    else:
        new_city = City(**json_data)
        new_city.state_id = state_id
        storage.save()
        return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ updates a City object """
    city = storage.get(City, city_id)
    json_data = request.get_json()
    if city is None:
        abort(404)
    elif not json_data:
        abort(400, description="Not a JSON")
    else:
        for key, value in json_data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        storage.save()
        return (jsonify(city.to_dict()), 200)
