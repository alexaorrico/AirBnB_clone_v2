#!/usr/bin/python3
"""Module for handling places in the API"""

# Import statements
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Get place information for all places in a specified city"""
    city_instance = storage.get("City", city_id)
    if city_instance is None:
        abort(404)
    places_list = []
    for place_instance in city_instance.places:
        places_list.append(place_instance.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Get place information for the specified place"""
    place_instance = storage.get("Place", place_id)
    if place_instance is None:
        abort(404)
    return jsonify(place_instance.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place based on its place_id"""
    place_instance = storage.get("Place", place_id)
    if place_instance is None:
        abort(404)
    place_instance.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Create a new place"""
    city_instance = storage.get("City", city_id)
    if city_instance is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user_instance = storage.get("User", kwargs['user_id'])
    if user_instance is None:
        abort(404)
    if 'name' not in kwargs:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs['city_id'] = city_id
    new_place = Place(**kwargs)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Update a place"""
    place_instance = storage.get("Place", place_id)
    if place_instance is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(place_instance, attr, val)
    place_instance.save()
    return jsonify(place_instance.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """Searches for a place"""
    if request.get_json() is not None:
        params = request.get_json()
        states = params.get('states', [])
        cities = params.get('cities', [])
        amenities = params.get('amenities', [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity_instance = storage.get('Amenity', amenity_id)
            if amenity_instance:
                amenity_objects.append(amenity_instance)
        if states == cities == []:
            places = storage.all('Place').values()
        else:
            places = []
            for state_id in states:
                state_instance = storage.get('State', state_id)
                state_cities = state_instance.cities
                for city_instance in state_cities:
                    if city_instance.id not in cities:
                        cities.append(city_instance.id)
            for city_id in cities:
                city_instance = storage.get('City', city_id)
                for place_instance in city_instance.places:
                    places.append(place_instance)
        confirmed_places = []
        for place_instance in places:
            place_amenities = place_instance.amenities
            confirmed_places.append(place_instance.to_dict())
            for amenity_instance in amenity_objects:
                if amenity_instance not in place_amenities:
                    confirmed_places.pop()
                    break
        return jsonify(confirmed_places)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
