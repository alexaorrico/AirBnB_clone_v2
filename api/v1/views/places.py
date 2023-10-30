#!/usr/bin/python3

"""Create a view for Place"""

from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views
from api.v1.views.places import *
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a place object by ID"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by ID"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get("User", data["user_id"])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    place = Place(**data)
    place.city_id = city.id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by ID"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    # Update the State object's attributes based on the JSON data
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = []
    all_cities = []
    all_places = storage.all("Place")

    if states == cities == amenities == []:
        places = all_places.values()
    else:
        if states:
            for state_id in states:
                state = storage.get("State", state_id)
                if state:
                    all_cities.extend(list(map(lambda s: s.id, state.cities)))

        all_cities.extend(cities)
        all_cities = list(set(all_cities))

        if all_cities:
            for city_id in all_cities:
                city = storage.get("City", city_id)
                if city:
                    places.extend(city.places)
        if amenities:
            places = [place for place in places
                      if all(amenity_id in place.amenities
                             for amenity_id in amenities)]

    result = list(map(lambda x: x.to_dict(), places))
    return jsonify(result)
