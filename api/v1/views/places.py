#!/usr/bin/python3
"""
This module defines a view for Place objects that handles
all default RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
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
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    user_id = data.get('user_id')
    if user_id is None:
        abort(400, 'Missing user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    name = data.get('name')
    if name is None:
        abort(400, 'Missing name')
    place = Place(city_id=city_id, user_id=user_id, name=name)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Retrieves all Place objects depending on the JSON in the request"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data:
        places = storage.all('Place').values()
        return jsonify([place.to_dict() for place in places])
    states = data.get('states')
    cities = data.get('cities')
    amenities = data.get('amenities')
    if not states and not cities and not amenities:
        places = storage.all('Place').values()
        return jsonify([place.to_dict() for place in places])
    places = []
    if states:
        for state_id in states:
            state = storage.get('State', state_id)
            if state:
                if not cities:
                    places.extend(state.places)
                else:
                    for city in state.cities:
                        if city.id in cities:
                            places.extend(city.places)
    if cities:
        for city_id in cities:
            city = storage.get('City', city_id)
            if city and city not in [state.cities for state in storage.all('State').values()]:
                places.extend(city.places)
    if amenities:
        for place in storage.all('Place').values():
            if all(amenity_id in [amenity.id for amenity in place.amenities] for amenity_id in amenities):
                places.append(place)
    return jsonify([place.to_dict() for place in places])
