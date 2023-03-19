#!/usr/bin/python3
""" flask module to manage the stored cities """
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage


@app_views.route(
    '/states/<string:state_id>/cities',
    strict_slashes=False,
    methods=['GET']
)
def all_cities(state_id):
    """ it retrieve all the cities """
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    cities_list = []
    for city in states.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route(
    '/cities/<string:city_id>',
    strict_slashes=False,
    methods=['GET']
)
def get_city(city_id):
    """ it get the city corresponding to the city_id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
    '/cities/<string:city_id>',
    strict_slashes=False,
    methods=['DELETE']
)
def delete_city(city_id):
    """ it delete the city corresponding to the city_id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/states/<string:state_id>/cities',
    strict_slashes=False,
    methods=['POST']
)
def create_city(state_id):
    """ it create an city from a http request
    the new city information is expected to be
    json string
    """
    states_city = storage.get(State, state_id)
    if states_city is None:
        abort(404)
    city_json = request.get_json()
    if city_json is None:
        abort(400, 'Not a JSON')
    if city_json.get('name') is None:
        abort(400, "Missing name")
    if city_json.get('state_id') is None:
        city_json['state_id'] = state_id
    city = City(**city_json)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route(
    '/cities/<string:city_id>',
    strict_slashes=False,
    methods=['PUT']
)
def update_city(city_id):
    """ it update an city """
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city_json = request.get_json()
    if city_json is None:
        abort(400, 'Not a JSON')

    for key, value in city_json.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
