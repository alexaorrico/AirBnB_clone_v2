#!/usr/bin/python3
"""route for places"""
from api.v1.views import app_views
from models.city import City
from models import storage
from models.place import Place
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/plalces", strict_slashes=False,
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


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["GET"])
def a_place(place_id):
    """retrieves a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_place(place_id):
    """deletes a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200
