#!/usr/bin/python3
"""
Creating a new view for Place objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place


@app_views.route('cities/<city_id>/places', strict_slashes=False,
                 methods=['Get'])
def list_of_places_for_city(city_id):
    """retrieves list of places based on id"""
    city = storage.get("City", city_id)
    places = []
    if city is None:
        abort(404)
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_on_id(place_id):
    """ get place by based on place id given """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())
