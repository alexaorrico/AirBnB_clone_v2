#!/usr/bin/python3
"""module for place and amenity relationship views"""
from flask import abort, json, request, jsonify, make_response
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/places/<string:place_id>/amenities",
                 strict_slashes=False, methods=["GET"])
def get_place_amenities(place_id):
    """retrives amenities that belong to a place"""
    required_place = storage.get(Place, place_id)
    if (not required_place):
        abort(404)

    result = []
    for amenity in required_place.amenities:
        result.append(amenity.to_dict())
    return jsonify(result)


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_place_amenity(place_id, amenity_id):
    required_place = storage.get(Place, place_id)
    if (not required_place):
        abort(404)

    required_amenity = storage.get(Amenity, amenity_id)
    if (not required_amenity):
        abort(404)

    if (storage_t != "db"):
        if not(amenity_id in required_place.amenities):
            abort(404)
    else:
        if not(required_amenity in required_place.amenities):
            abort(404)

    if (storage_t != "db"):
        required_place.amenities.remove(amenity_id)
        required_place.save()
        return jsonify({}), 200
    else:
        required_place.amenities.remove(required_amenity)
        required_place.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["POST"])
def link_place_amenity(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    required_place = storage.get(Place, place_id)
    if (not required_place):
        abort(404)

    required_amenity = storage.get(Amenity, amenity_id)
    if (not required_amenity):
        abort(404)

    if (storage_t != "db"):
        if amenity_id in required_place.amenities:
            return jsonify(required_amenity.to_dict()), 200
    else:
        if required_amenity in required_place.amenities:
            return jsonify(required_amenity.to_dict()), 200

    if (storage_t != "db"):
        required_place.amenities = required_amenity
        required_place.save()
        return jsonify(required_amenity.to_dict()), 201
    else:
        required_place.amenities.append(required_amenity)
        required_place.save()
        return jsonify(required_amenity.to_dict()), 201
