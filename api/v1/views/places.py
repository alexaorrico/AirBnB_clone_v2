#!/usr/bin/python3
"""place obj API"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.city import City
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


@app_views.route('/places_search', methods=['GET'], strict_slashes=False)
def get_places_search():
    place_search = request.get_json()
    if place_search is None:
        abort(404, 'Not a JSON')
    if len(place_search) and place_search:
        states = place_search.get('states', None)
        cities = place_search.get('cities', None)
        amenities = place_search.get('amenities', None)