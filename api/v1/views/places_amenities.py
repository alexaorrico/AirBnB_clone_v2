#!/usr/bin/python3
"""view for places_amenities.py objects handles all
   default RESTFul API actions"""
import os
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def place_amenities(place_id):
    """Retrieves the list of all amenity objects of a place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        objects = place.amenities
    else:
        objects = place.amenity_ids

    data = []
    for amenity in objects:
        data.append(amenity.to_dict())
    return jsonify(data)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_places_amenity(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        objects = place.amenities
    else:
        objects = place.amenity_ids
    if amenity not in objects:
        abort(404)

    objects.remove(amenity)
    place.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        objects = place.amenities
    else:
        objects = place.amenity_ids
    if amenity in objects:
        return jsonify(amenity.to_dict()), 200

    objects.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
