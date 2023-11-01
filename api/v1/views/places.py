#!/usr/bin/python3
"""Place-related API endpoints"""

from flask import jsonify, request, abort
from . import app_views, Place, storage


@app_views.route("/cities/<city_id>/places",
                 methods=["GET", "POST"], strict_slashes=False)
def get_places(city_id):
    """Creates places for a city with the given city_id."""
    places_list = []
    ct = storage.get("City", str(city_id))
    for place in ct.places:
        places_list.append(place.to_json())
    return jsonify(places_list)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a new place for the given city_id."""
    place_data = request.get_json(silent=True)
    if place_data is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", place_data.get("user_id")):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in place_data:
        abort(400, 'Missing user_id')
    if "name" not in place_data:
        abort(400, 'Missing name')
    place_data["city_id"] = city_id
    added_place = Place(**place_data)
    added_place.save()
    response = jsonify(added_place.to_json())
    response.status_code = 201
    return response


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place_id(place_id):
    """Provides place info for a given place using the given place_id."""
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    return jsonify(place.to_json())


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place_id(place_id):
    """Provides update functionality for places with a place id."""
    update_data = request.get_json(silent=True)
    if update_data is None:
        abort(400, 'Not a JSON')
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    for key, value in update_data.items():
        if key not in ["id",
                       "created_at",
                       "updated_at",
                       "user_id",
                       "city_id"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_json())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """Removes a place from the database based on the given place_id"""
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})
