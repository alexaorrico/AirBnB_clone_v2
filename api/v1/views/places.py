#!/usr/bin/python3
"""
Contains the places view for the AirBnB clone v3 API.
Handles all default RESTful API actions for Place objects.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_places_for_city(city_id):
    """Retrieves all Place objects for a specified City."""
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a specific Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place in a specified City."""
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404, description="User not found")
    if 'name' not in data:
        abort(400, description="Missing name")
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a specific Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a specific Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves Place objects based on a JSON search criteria."""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    places = perform_search(data)
    result = [place.to_dict() for place in places]
    return jsonify(result)


def perform_search(data):
    """Performs the actual search based on states, cities, and amenities."""
    places = set()
    if data.get('states'):
        for state_id in data['states']:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.update(city.places)
    if data.get('cities'):
        for city_id in data['cities']:
            city = storage.get(City, city_id)
            if city:
                places.update(city.places)
    if data.get('amenities'):
        places_with_amenities = set()
        for place in places:
            if check_place_amenities(place, data['amenities']):
                places_with_amenities.add(place)
        places = places_with_amenities
    return places


def check_place_amenities(place, amenity_ids):
    """Check if all specified amenities are in a place's amenities."""
    place_amenity_ids = [a.id for a in place.amenities]
    return all(amenity_id in place_amenity_ids for amenity_id in amenity_ids)
