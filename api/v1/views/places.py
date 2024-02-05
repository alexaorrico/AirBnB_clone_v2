#!/usr/bin/python3
"""
Module for handling RESTful API actions for Place objects.
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Searches for places based on JSON in the request body.
    """
    try:
        json_data = request.get_json()

        if not json_data:
            abort(400, description="Not a JSON")

        states = json_data.get('states', [])
        cities = json_data.get('cities', [])
        amenities = json_data.get('amenities', [])

        places = storage.all(Place).values()

        if not states and not cities and not amenities:
            return jsonify([place.to_dict() for place in places])

        results = []

        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    results.extend(city.places)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                results.extend(city.places)

        if amenities:
            results = [place for place in results
                       if all(amenity.id in place.amenity_ids
                              for amenity in amenities)]

        return jsonify([place.to_dict() for place in results])

    except Exception as e:
        return jsonify({"error": str(e)}), 500
