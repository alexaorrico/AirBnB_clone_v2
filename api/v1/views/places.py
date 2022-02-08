#!/usr/bin/python3
"""view for places objects"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """new endpoint: POST /api/v1/places_search that retrieves all Place
    objects depending of the JSON in the body of the request."""

    if request.get_json() is not None:
        params = request.get_json()
        states = params.get('states', [])
        cities = params.get('cities', [])
        amenities = params.get('amenities', [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity = storage.get('Amenity', amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        if states == cities == []:
            places = storage.all('Place').values()
        else:
            places = []
            for state_id in states:
                state = storage.get('State', state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get('City', city_id)
                for place in city.places:
                    places.append(place)
        confirmed_places = []
        for place in places:
            place_amenities = place.amenities
            confirmed_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    confirmed_places.pop()
                    break
        return jsonify(confirmed_places)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
