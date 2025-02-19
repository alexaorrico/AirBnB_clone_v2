#!/usr/bin/python3
"""This creates a view for place"""

from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
import requests
import json
from os import getenv


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """This retrieves a list of all Place objects"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """This retrieves a place object by Id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """This deletes a place object by Id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """This creates a place object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get("User", data["user_id"])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    place = Place(**data)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """This updates a place object by Id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """This retrieves all place objects depending on the request"""
    if not request.json:
        abort(400, 'Not a JSON')

    states = request.json.get('states', [])
    cities = request.json.get('cities', [])
    amenities = request.json.get('amenities', [])

    if not states and not cities and not amenities:
        places = storage.all('Place').values()
        return jsonify([place.to_dict() for place in places])

    place_ids = set()

    for state_id in states:
        state = storage.get('State', state_id)
        if state:
            for city in state.cities:
                for place in city.places:
                    place_ids.add(place.id)

    for city_id in cities:
        city = storage.get('City', city_id)
        if city:
            for place in city.places:
                place_ids.add(place.id)

    if not place_ids:
        return jsonify([])

    if amenities:
        place_ids = filter_by_amenities(place_ids, amenities)

    places = [storage.get('Place', place_id).to_dict() for place_id in place_ids]
    return jsonify(places)


def filter_by_amenities(place_ids, amenities):
    filtered_place_ids = set()
    """This filters amenities by place ids"""

    for place_id in place_ids:
        place = storage.get('Place', place_id)
        if place and all(amenity_id in place.amenities for amenity_id in amenities):
            filtered_place_ids.add(place_id)

    return filtered_place_ids
