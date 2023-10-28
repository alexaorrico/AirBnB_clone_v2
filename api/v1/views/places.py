#!/usr/bin/python3
""" holds class Place"""
from api.v1.views import app_views
from models.place import Place
from models import storage
from flask import Flask, jsonify, abort, request


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """ search for a place """

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    states = data.get("states", [])
    cities = data.get("cities", [])
    amenities = data.get("amenities", [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    places_set = set()
    if states:
        for state_id in states:
            state = storage.get("State", state_id)
            if state is not None:
                for city in state.cities:
                    places_set.update(city.places)

    if cities:
        for city_id in cities:
            city = storage.get("City", city_id)
            if city is not None:
                places_set.update(city.places)

    if amenities:
        amenities_set = set(amenities)
        places_set = {place for place in places_set if amenities_set.issubset(
            {amenity.id for amenity in place.amenities})}

    return jsonify([place.to_dict() for place in places_set])
