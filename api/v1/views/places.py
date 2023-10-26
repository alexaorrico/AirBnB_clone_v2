#!/usr/bin/python3
"""
Place view for the AirBnB API.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage, Place, City, User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieve a list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new Place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    try:
        search_data = request.get_json()
    except:
        abort(400, description="Not a JSON")

    states = search_data.get("states", [])
    cities = search_data.get("cities", [])
    amenities = search_data.get("amenities", [])

    places = []

    # If no specific criteria are provided, retrieve all Place objects
    if not states and not cities and not amenities:
        places = list(storage.all(Place).values())

    # Search by states
    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                cities_in_state = state.cities
                for city in cities_in_state:
                    places.extend(city.places)

    # Search by individual cities
    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)

    # Filter by amenities
    if amenities:
        places = [place for place in places if all(amenity_id in place.amenity_ids() for amenity_id in amenities)]

    return jsonify([place.to_dict() for place in places])