#!/usr/bin/python3
"""Places module"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity


@app_views.route('/places_search',
                 methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Searches for places based n JSON in request body"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JOSN')

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places_result = []

    if not states and not cities and not amenities:
        place_result = [
                        place.to_dict()
                        for place in storage.all(Place).values()
        ]
                        place.to_dict() for place in storage.all(
                            Place).values()
                       ]
    else:
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    places_result.extend([
                                          place.to_dict()
                                          for city in state.cities
                                          for place in city.places
                            place.to_dict(
                            ) for city in state.cities for place in city.places
                    ])

        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    places_result.extend([
                            place.to_dict() for place in city.places
                    ])

        if amenities:
            amnenities_set = set(amenities)
            places_result = [
                             place for place in places_result
                             if amenities_set.issubset(
                                 place.get('amenities', []))]

                    place for place in places_result if amenities_set.issubset(
                        place.get('amenities', []))]

    return jsonify(places_result)
