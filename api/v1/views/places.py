#!/usr/bin/python3
"""places.py"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search for places based on JSON request"""
    request_json = request.get_json()

    if request_json is None:
        abort(400, 'Not a JSON')

    states_ids = request_json.get('states', [])
    cities_ids = request_json.get('cities', [])
    amenities_ids = request_json.get('amenities', [])

    if not states_ids and not cities_ids and not amenities_ids:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    places_result = set()

    if states_ids:
        for state_id in states_ids:
            state = storage.get(State, state_id)
            if state:
                places_result.update(state.places)

    if cities_ids:
        for city_id in cities_ids:
            city = storage.get(City, city_id)
            if city:
                places_result.update(city.places)

    if amenities_ids:
        amenities = [storage.get(Amenity, amenity_id) for amenity_id in amenities_ids]
        places_result = [place for place in places_result if all(amenity in place.amenities for amenity in amenities)]

    return jsonify([place.to_dict() for place in places_result])
