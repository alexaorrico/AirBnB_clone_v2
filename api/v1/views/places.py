#!/usr/bin/python3
"""
Module for Place objects that handles all default RESTFul API actions.
"""

from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a specific Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a specific Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place in a specified City.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a specific Place object.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves Place objects based on a JSON search criteria.
    """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    places = handle_search(data)
    return jsonify([place.to_dict() for place in places])


def handle_search(data):
    """
    Handles the search logic for places.
    """
    if not data or all(
            not data.get(key) for key in ['states', 'cities', 'amenities']
            ):
        return list(storage.all(Place).values())
    else:
        return search_places(data)


def search_places(data):
    """
    Searches for places based on states, cities, and amenities.
    """
    places = set()
    if 'states' in data:
        for state_id in data['states']:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.update(city.places)
    if 'cities' in data:
        for city_id in data['cities']:
            city = storage.get(City, city_id)
            if city:
                places.update(city.places)
    if 'amenities' in data:
        filtered_places = {place for place in places
                           if check_place_amenities(place, data['amenities'])}
        return list(filtered_places)
    return list(places)


def check_place_amenities(place, amenity_ids):
    """
    Check if all amenity_ids are in a place's amenities.
    """
    place_amenity_ids = [amenity.id for amenity in place.amenities]
    return all(amenity_id in place_amenity_ids for amenity_id in amenity_ids)
