#!/usr/bin/python3
"""
Places view
"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State

app = Flask(__name__)


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, "Not a JSON")
    if 'user_id' not in content:
        abort(400, "Missing user_id")
    if 'name' not in content:
        abort(400, "Missing name")
    user = storage.get(User, content['user_id'])
    if user is None:
        abort(404)
    new_place = Place(city_id=city_id, **content)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, "Not a JSON")
    for key, value in content.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Searches for places based on JSON in the request body"""

    try:
        search_params = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    if not search_params or not any(search_params.values()):
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    states = search_params.get('states', [])
    cities = search_params.get('cities', [])
    amenities = search_params.get('amenities', [])

    if not isinstance(states, list) or not isinstance(cities, list) or not isinstance(amenities, list):
        abort(400, "Invalid JSON")

    places_result = set()

    # Filter places by states
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            places_result.update(state.places)

    # Filter places by cities
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            places_result.update(city.places)

    # Filter places by amenities
    if amenities:
        amenities_set = set(amenities)
        places_result = [
            place for place in places_result if amenities_set.issubset(place.amenities)]

    return jsonify([place.to_dict() for place in places_result])
