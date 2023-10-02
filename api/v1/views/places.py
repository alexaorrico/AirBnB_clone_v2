#!/usr/bin/python3
"""
This module defines a Flask web application that
provides a RESTful API for Places objects.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City.
    """
    city = next((city for city in storage.all(City).values()
                 if city.id == city_id), None)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in storage.all(Place).values()
              if place.city_id == city_id]
    return jsonify(places), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object.
    """
    place = next((place for place in storage.all(Place).values()
                 if place.id == place_id), None)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place object.
    """
    place = next((place for place in storage.all(Place).values()
                 if place.id == place_id), None)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place.
    """
    city = next((city for city in storage.all(City).values()
                 if city.id == city_id), None)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = next((user for user in storage.all(User).values()
                 if user.id == data['user_id']), None)
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object.
    """
    place = next((place for place in storage.all(Place).values()
                 if place.id == place_id), None)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    Retrieves all Place objects based on the JSON in the body of the request.
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if not data:
        places = [place.to_dict() for place in storage.all(Place).values()]
        return jsonify(places), 200
    places = []
    if 'states' in data and data['states']:
        states = [storage.get(State, state_id) for state_id in data['states']]
        for state in states:
            if state:
                for city in state.cities:
                    for place in city.places:
                        places.append(place.to_dict())
    if 'cities' in data and data['cities']:
        cities = [storage.get(City, city_id) for city_id in data['cities']]
        for city in cities:
            if city:
                for place in city.places:
                    if place.to_dict() not in places:
                        places.append(place.to_dict())
    if 'amenities' in data and data['amenities']:
        amenities = [storage.get(Amenity, amenity_id)
                     for amenity_id in data['amenities']]
        places = [place for place in places if
                  all(amenity in place.amenities for amenity in amenities)]
    return jsonify(places), 200
