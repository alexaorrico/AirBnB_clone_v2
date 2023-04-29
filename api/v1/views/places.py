#!/usr/bin/python3
"""This module handles all default Restful API actions for Place objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, Place, State, City, Amenity
from flasgger.utils import swag_from


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Searches for places based on JSON data in request body"""
    json_data = request.get_json()

    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400

    state_ids = json_data.get('states')
    city_ids = json_data.get('cities')
    amenity_ids = json_data.get('amenities')

    if not state_ids and not city_ids and not amenity_ids:
        return jsonify([p.to_dict() for p in storage.all(Place).values()])

    places = []
    for place in storage.all(Place).values():
        if state_ids and place.city.state_id not in state_ids:
            continue
        if city_ids and place.city_id not in city_ids:
            continue
        if amenity_ids:
            place_amenity_ids = {amenity.id for amenity in place.amenities}
            if not set(amenity_ids).issubset(place_amenity_ids):
                continue
        places.append(place.to_dict())

    return jsonify(places)


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_by_city(city_id):
    """Retrieves all Place objects in a given City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify([place.to_dict() for place in city.places])


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
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if 'user_id' not in json_data:
        return jsonify({"error": "Missing user_id"}), 400

    user_id = json_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if 'name' not in json_data:
        return jsonify({"error": "Missing name"}), 400

    place = Place(city_id=city_id, user_id=user_id, name=json_data['name'])
    for k, v in json_data.items():
        if k not in ('id', 'city_id', 'user_id', 'created_at', 'updated_at',
                     'name'):
            setattr(place, k, v)

    storage.new(place)
    storage.save()
