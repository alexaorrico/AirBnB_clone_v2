#!/usr/bin/python3
"""View for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_all_city_places(city_id):
    """return all the places linked to the city with city_id"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """return a place by id in the database"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    return jsonify(place.to_dict()), 200
