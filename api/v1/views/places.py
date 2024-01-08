#!/usr/bin/python3
"""
View for places that handles all RESTful API actions
"""
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """Returns a list of all places in a given city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Returns a single place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """"Deletes a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Adds a new place in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    if storage.get(User, data.get('user_id')) is None:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    special_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in special_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


def has_amenities(place, amenities):
    """Check if a place has any of the passed amenities"""
    place_amenities = [amenity.id for amenity in place.amenities]
    return bool(set(place_amenities) & set(amenities))


@app_views.route('/places_search', methods=['POST'])
def search_places():
    """Returns a list of places that matches the search criteria"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    state_ids = data.get('states', [])
    city_ids = data.get('cities', [])
    amenity_ids = data.get('amenities', [])
    city_ids = set(city_ids)
    for state_id in state_ids:
        state = storage.get(State, state_id)
        if state:
            city_ids.update([city.id for city in state.cities])
    city_ids = list(city_ids)
    places = storage.all(Place).values()
    if city_ids:
        places = [place for place in places if place.city_id in city_ids]
    if not amenity_ids:
        return jsonify([place.to_dict() for place in places])
    return jsonify([place.to_dict() for place in places if
                    has_amenities(place, amenity_ids)])
