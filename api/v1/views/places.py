#!/usr/bin/python3

"""Places view."""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity

app = Flask(__name__)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search for places based on JSON in the request body."""
    try:
        request_json = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    if not request_json:
        places = [place.to_dict() for place in storage.all(Place).values()]
        return jsonify(places)

    states = request_json.get('states', [])
    cities = request_json.get('cities', [])
    amenities = request_json.get('amenities', [])

    places = set()

    # Include places from each State in states
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            places.update(state.places)

    # Include places from each City in cities
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            places.update(city.places)

    # Include places from each City in states (cities are inclusive)
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            places.update(state.places)

    # Filter places by amenities
    if amenities:
        places = [place for place in places if all(amenity_id in place.amenity_ids for amenity_id in amenities)]

    return jsonify([place.to_dict() for place in places])

