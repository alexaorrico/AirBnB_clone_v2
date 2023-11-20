#!/usr/bin/python3
"""
View for Cities objects that will handle all default
RESTful API actions
"""
# Allison Edited 11/20 3:45 PM
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    """retrieves the list of all City objects"""
    all_cities = storage.all(City).values()
    cities_list = []
    for city in all_cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/city/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    """retrieves a city object when a specific city ID is provided
        will return 404 error if city is not found."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """deletes city object specified by city id, returns a 404 error
        if city is not found, returns empty dictionary with status code 200"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def new_city():
    """Creates a new city - transforms the HTTP body request to a dictionary
    handles error raises, returns new city with status code 201"""

    new_data = request.get_json()

    if new_data is None:
        abort(400, description="Not a JSON")
    if 'name' not in new_data:
        abort(400, description="Missing name")

    new_city = City(**new_data)
    """** -> double asterisks unpacks a dictionary and passes
    the key-value pairs as arguments to the city constructor!"""
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_da_city(city_id):
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    key_ignore = ['id', 'created_at', 'updated_at']

    new_data = request.get_json()
    for key, value in new_data.items():
        if key not in key_ignore:
            setattr(city, key, value)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
