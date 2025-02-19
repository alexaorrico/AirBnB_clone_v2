#!/usr/bin/python3
"""
Handles RESTful API actions for Place objects
"""
from flask import jsonify, abort, request
from models.place import Place
from models import storage
from api.v1.views import app_views


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    Retrieves Place objects based on the JSON in the request body
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    place_ids = set()

    # Search by states
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                place_ids.update({place.id for place in city.places})

    # Search by cities
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            place_ids.update({place.id for place in city.places})

    # Search by amenities
    if amenities:
        filtered_place_ids = set()
        for place_id in place_ids:
            place = storage.get(Place, place_id)
            if place:
                if all(amenity_id in place.amenities for amenity_id in amenities):
                    filtered_place_ids.add(place_id)
        place_ids = filtered_place_ids

    places = [storage.get(Place, place_id) for place_id in place_ids]
    places = [place for place in places if place]

    return jsonify([place.to_dict() for place in places])

