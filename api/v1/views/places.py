#!/usr/bin/python3
'''routes for Place objects'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.state import State
import json


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    '''Retrieve all Place objects of a City'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    '''Retrieve a Place object'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''Delete a Place object'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''Create a Place object'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    elif 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)


    place = Place(city_id=city_id, user_id=user_id, **data)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''Update a Place object'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    '''Search for places based on JSON request'''
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    states = data.get("states", [])
    cities = data.get("cities", [])
    amenities = data.get("amenities", [])

    places = []

    if not states and not cities and not amenities:
        places = [place.to_dict() for place in storage.all(Place).values()]
    else:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                places.extend([place.to_dict() for city in state.cities
                              for place in city.places])

        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.extend([place.to_dict() for place in city.places])

    if amenities:
        amenities_set = set(amenities)
        places = [place for place in places
                  if amenities_set.issubset(place.get("amenities", []))]

    return jsonify(places)
