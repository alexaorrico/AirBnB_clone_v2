#!/usr/bin/python3
"""RESTFul API"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def list_places_b_city(city_id):
    """list of all Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places), 200


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place_b_id(place_id):
    """Get Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_b_id(place_id):
    """Delete Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place_id(city_id):
    """new Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    data['city_id'] = city_id
    nw_place = Place(**data)
    storage.new(nw_place)
    storage.save()
    return jsonify(nw_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place_b_id(place_id):
    """Update Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ig_key = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ig_key:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search',
                 methods=['POST'], strict_slashes=False)
def places_search_places():
    """Retrieves all Place objects"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    places = set()

    if not data or (not data.get('states') and not data.get('cities') and not data.get('amenities')):
        places = set(storage.all(Place).values())
    else:
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
        amenities_ids = data['amenities']
        filtrd_places = set()
        for place in places:
            place_amenities_ids = [amenity.id for amenity in place.amenities]
            if all(amenity_id in place_amenities_ids for amenity_id in amenities_ids):
                filtrd_places.add(place)
        places = filtrd_places

    plcs_lst = [place.to_dict() for place in places]
    return jsonify(plcs_lst), 200
