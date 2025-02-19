#!/usr/bin/python3
""" API endpoints for places """

from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User

from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'])
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'])
def create_place(city_id):
    """Creates a new Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    forbidden_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in forbidden_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search',
                 methods=['POST'])
def search_places():
    """Searches for places"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = []
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        for place in storage.all(Place).values():
            if place.city_id in cities:
                places.append(place)
            elif place.state_id in states:
                places.append(place)
        if amenities:
            places = [place for place in places
                      if all(amenity in place.amenities
                             for amenity in amenities)]
    return jsonify([place.to_dict() for place in places])
