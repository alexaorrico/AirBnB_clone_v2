#!/usr/bin/python3
"""This module defines a view for Place objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """Retrieves the list of all Place objects of a City
    or creates a new one"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places = city.places
        return jsonify([place.to_dict() for place in places])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)
        if 'name' not in data:
            abort(400, 'Missing name')
        place = Place(**data)
        place.city_id = city_id
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place(place_id):
    """Retrieves, deletes or updates a Place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves all Place objects depending of the JSON
    in the body of the request"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])
    places = []
    """If states list is not empty, include all Place objects
    for each State id listed"""
    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.extend(city.places)
    """If cities list is not empty, include all
    Place objects for each City id listed"""
    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)
    # If both states and cities lists are empty, include all Place objects
    if not states and not cities:
        places = storage.all(Place).values()
    # If amenities list is not empty, filter the Place objects by amenities
    if amenities:
        places = [place for place in places if all(amenity in place.amenities
                                                   for amenity in amenities)]
    # Return the list of Place objects as JSON
    return jsonify([place.to_dict() for place in places])
