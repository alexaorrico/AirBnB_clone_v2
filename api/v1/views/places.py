#!/usr/bin/python3
"""
Handles all default RESTFul API actions for Place objects
"""

from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place/places_search.yml', methods=['POST'])
def places_search():
    """
    Retrieves all Place objects depending on the JSON in the body of the request
    """
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = []

    if not states and not cities:
        # If the JSON body is empty or each list of all keys are empty: retrieve all Place objects
        places = [place.to_dict() for place in storage.all(Place).values()]
    else:
        # If states list is not empty, include all Place objects for each State id listed
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                places.extend([place.to_dict() for city in state.cities for place in city.places])

        # If cities list is not empty, include all Place objects for each City id listed
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.extend([place.to_dict() for place in city.places])

    # Filter places based on amenities list
    if amenities:
        places = [place for place in places if all(amenity.id in place['amenities'] for amenity in amenities)]

    return jsonify(places)
