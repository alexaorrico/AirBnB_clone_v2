#!/usr/bin/python3
"""route for places"""
from api.v1.views import app_views
from models.city import City
from models import storage
from models.place import Place
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/plalces", strict_slashes=True,
                 methods=["GET"])
def get_places(city_id):
    """get the places in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    all_places = []
    for place in city.places:
        all_places.append(place.to_dict())
    return jsonify(all_places)
