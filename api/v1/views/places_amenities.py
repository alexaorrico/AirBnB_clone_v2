#!/usr/bin/python3

"""handles all default RESTFul API actions"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE", "POST"])
def place_amenities(place_id, amenity_id=None):
    """Handles GET request"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
        return

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids

    if request.method == "GET":
        return jsonify([amenity.to_dict() for amenity in place_amenities])

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None or amenity not in place_amenities:
        abort(404)
        return

    if request.method == "DELETE":
        place_amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200

    elif request.method == "POST":
        if amenity in place_amenities:
            return jsonify(amenity.to_dict()), 200
        place_amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
