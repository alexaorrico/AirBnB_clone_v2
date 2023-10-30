#!/usr/bin/python3
"""Places API views"""
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_places(city_id):
    """Retrieves a list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a specific Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a specific Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new Place associated with a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if storage.get(User, data["user_id"]) is None:
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")
    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search for Place objects based on JSON request data."""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    states = data.get("states", [])
    cities = data.get("cities", [])
    amenities = data.get("amenities", [])
    all_places = storage.all(Place).values()
    places_to_return = filter_places(all_places, states, cities, amenities)
    places_to_dict = [place.to_dict() for place in places_to_return]
    return jsonify(places_to_dict)


def filter_places(all_places, states, cities, amenities):
    """Filter Place objects based on the specified search criteria."""
    places_to_return = set()
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            cities.extend([city.id for city in state.cities])
        else:
            abort(404)
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            places_to_return.update(city.places)
        else:
            abort(404)
    if amenities:
        places_to_return = {
            place for place in places_to_return if all(
                amenity in place.amenities for amenity in amenities)
        }
    return list(places_to_return)
