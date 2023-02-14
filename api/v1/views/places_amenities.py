#!/usr/bin/python3
"""Module for Place related endpoints"""
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, make_response, abort, request
from models import storage

model = "Amenity"
parent_model = "Place"


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=["GET"])
def get_amenities(place_id):
    """GET /place api route"""
    return get_models(parent_model, place_id, "amenities")


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["DELETE", "POST"])
def process_amenity(place_id, amenity_id):
    """Process request type"""
    if request.method == "DELETE":
        return delete_amenity(place_id, amenity_id)
    else:
        return post_amenity(place_id, amenity_id)


def delete_amenity(place_id, amenity_id):
    """DELETE /amenity api route"""
    place = storage.get(parent_model, place_id)
    if not place:
        return make_response(jsonify({"error": "Not found"}), 404)
    amenity = storage.get(model, amenity_id)
    if not amenity:
        return make_response(jsonify({"error": "Not found"}), 404)

    if amenity not in place.amenities:
        return make_response(jsonify({"error": "Not found"}), 404)

    # storage.delete(amenity)
    # if getenv("HBNB_TYPE_STORAGE") != "db":
    place.amenities.remove(amenity)
    # else:
    #    storage.delete(amenity)

    storage.save()
    return make_response(jsonify({}), 200)


def post_amenity(place_id, amenity_id):
    """POST /amenities api route"""
    place = storage.get(parent_model, place_id)
    if not place:
        return make_response(jsonify({"error": "Not found"}), 404)
    amenity = storage.get(model, amenity_id)
    if not amenity:
        return make_response(jsonify({"error": "Not found"}), 404)

    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)

    place.amenities.append(amenity)

    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
