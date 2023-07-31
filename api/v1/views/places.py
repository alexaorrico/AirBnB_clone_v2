#!/usr/bin/python3
"""place obj API"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from os import getenv
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_in_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """Get all places or a places whose id is specified"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Create a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place = request.get_json()
    if not place:
        abort(400, description="Not a JSON")
    if 'user_id' not in place:
        abort(400, description="Missing user_id")
    user = storage.get(User, place.get('user_id'))
    if user is None:
        abort(404)
    if 'name' not in place:
        abort(400, description="Missing name")
    place['city_id'] = city_id
    obj = Place(**place)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Update a place object"""
    place = storage.get(Place, place_id)
    fixed_data = ['id', 'user_id', 'created_at', 'updated_at']
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in fixed_data:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    place_search = request.get_json()
    if place_search and len(place_search):
        states = place_search.get('states', None)
        cities = place_search.get('cities', None)
        amenities = place_search.get('amenities', None)
        if states and cities:
            place_list = [states, cities]
        elif states and not cities:
            place_list = [states]
        elif cities and not states:
            place_list = [cities]
        else:
            place_list = None
    else:
        place_list = None
        amenities = None

    if place_list:
        places = []
        for place_location in place_list:
            if place_location == states:
                for state_id in place_location:
                    state = storage.get(State, state_id)
                    for city in state.cities:
                        for place in city.places:
                            if place not in places and\
                              check_amenities(place, amenities):
                                pl_list = place.to_dict()
                                pl_list.pop('amenities', None)
                                places.append(pl_list)
            else:
                for city_id in place_location:
                    city = storage.get(City, city_id)
                    if city:
                        for place in city.places:
                            if place not in places and\
                              check_amenities(place, amenities):
                                pl_list = place.to_dict()
                                pl_list.pop('amenities', None)
                                places.append(pl_list)
        return make_response(jsonify(places))
    else:
        places = storage.all(Place)
        places_list = []
        for place in places.values():
            if check_amenities(place, amenities):
                pl_list = place.to_dict()
                pl_list.pop('amenities', None)
                places_list.append(pl_list)
        return jsonify(places_list)


def check_amenities(place, amenities_id):
    if amenities_id is not None:
        for amenity_id in amenities_id:
            amenities = storage.get(Amenity, amenity_id)
            if amenities not in place.amenities:
                return False
    return True
