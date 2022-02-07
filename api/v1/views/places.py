#!/usr/bin/python3
"""view for places objects"""
from tkinter import N
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """Retrieves the list of all places given an City"""
    places_list = []
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', strict_slashes=False)
def place_by_id(place_id):
    """Retrieves a place by a given ID"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    '/places/<place_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def delete_place(place_id):
    """Deletes a place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/cities/<city_id>/places',
    methods=['POST'],
    strict_slashes=False
    )
def create_place(city_id):
    """Creates a place object"""
    request_data = request.get_json()
    state = storage.get("City", city_id)
    if state is None:
        abort(404)
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request_data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get('User', request_data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request_data:
        return jsonify({"error": "Missing name"}), 400
    name = request.get_json().get('name')
    user_id = request.get_json().get('user_id')
    obj = Place(name=name, user_id=user_id, city_id=city_id)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in request_data.items():
        setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search/', methods=['POST'], strict_slashes=False)
def search_place():
    """that retrieves all Place objects depending
    of the JSON in the body of the request"""

    request_data = request.get_json()
    places_list = []

    if request_data is None:
        abort(404, description="No a JSON")

    if request_data or not len(request_data):
        states = request_data.get('states', None)
        cities = request_data.get('cities', None)
        amenities = request_data.get('amenities', None)

    if not request_data or not len(request_data) or (
       not states and
       not cities and
       not amenities):
        places = storage.all(Place).values()
        for place in places:
            places_list.append(place.to_dict())
        return jsonify(places_list)

    if states:
        obj = [storage.get(State, state_id) for state_id in states]
        for state in obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            places_list.append(place)

    if cities:
        obj = [storage.get(City, city_id) for city_id in cities]
        for city in obj:
            if city:
                for place in city.places:
                    if place not in places_list:
                        places_list.append(place)

    if amenities:
        if not places_list:
            places_list = storage.all(Place).values()
        obj = [storage.get(Amenity, amenity_id) for amenity_id in amenities]
        places_list = [place for place in places_list
                       if all([amenity in place.amenities
                               for amenity in obj])]

    confirmed_places = []
    for place in places_list:
        cp = confirmed_places.to_dict()
        cp.pop('amenities', None)
        confirmed_places.append(cp)

    return jsonify(confirmed_places)
