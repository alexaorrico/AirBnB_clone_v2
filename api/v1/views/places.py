#!/usr/bin/python3
"""Places API views"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Search for Place objects based on JSON request data."""
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    states = data.get("states", [])
    cities = data.get("cities", [])
    amenities = data.get("amenities", [])

    if not states and not cities and not amenities:
        places = storage.all("Place").values()
    else:
        places = []
        for state_id in states:
            state = storage.get("State", state_id)
            if state:
                places.extend(state.cities)

        for city_id in cities:
            city = storage.get("City", city_id)
            if city and city not in places:
                places.append(city)

    result_places = []
    for place in places:
        if amenities:
            place_amenities = {amenity.id for amenity in place.amenities}
            if set(amenities).issubset(place_amenities):
                result_places.append(place.to_dict())
        else:
            result_places.append(place.to_dict())

    return jsonify(result_places)
