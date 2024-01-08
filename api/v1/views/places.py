#!/usr/bin/python3
"""places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """Search for places based on JSON parameters"""
    try:
        request_json = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')

    if not request_json or not isinstance(request_json, dict):
        return jsonify([place.to_dict() for place in storage.all(Place).values()])

    states = request_json.get('states', [])
    cities = request_json.get('cities', [])
    amenities = request_json.get('amenities', [])

    if not states and not cities and not amenities:
        return jsonify([place.to_dict() for place in storage.all(Place).values()])

    places_result = set()

    # Filter by states
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                places_result.update(city.places)

    # Filter by cities
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            places_result.update(city.places)

    # Filter by amenities
    for amenity_id in amenities:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            places_result = {place for place in places_result if amenity in place.amenities}

    return jsonify([place.to_dict() for place in places_result])


# ... (existing routes for listing, creating, updating, and deleting places)
