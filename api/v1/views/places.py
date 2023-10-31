#!/usr/bin/python3
"""
Place view for the AirBnB API.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieve a list of all Place objects of a City"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object by ID"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object by ID"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a new Place object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a Place object by ID"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """searches for a place"""
    if request.get_json() is not None:
        search_parameters = request.get_json()
        states = search_parameters.get('states', [])
        cities = search_parameters.get('cities', [])
        amenities = search_parameters.get('amenities', [])
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
        filtered_places = []
        for place in places:
            place_amenities = place.amenities
            filtered_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    filtered_places.pop()
                    break
        return jsonify(filtered_places)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
