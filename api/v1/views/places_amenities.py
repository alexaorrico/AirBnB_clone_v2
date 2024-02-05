#!/usr/bin/python3
"""Places Amenities RESTAPI"""
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request, make_response
from os import getenv


@app_views.route("/places/<place_id>/amenities", strict_slashes=False)
def get_place_amenities(place_id):  # Get all amenities of a place
    place = storage.get(Place, place_id)
    if place:
        if getenv("HBNB_TYPE_STORAGE") == "db":
            return jsonify([amenity.to_dict() for amenity in place.amenities])
        else:
            return jsonify(
                [
                    storage.get(Amenity, amenity_id).to_dict()
                    for amenity_id in place.amenities
                ]
            )
    abort(404)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    strict_slashes=False,
    methods=["DELETE"],
)
def delete_place_amenity(
    place_id, amenity_id
):  # Deletes an amenity object from a place
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity:
        if getenv("HBNB_TYPE_STORAGE") == "db":
            if amenity in place.amenities:
                place.amenities.remove(amenity)
            else:
                abort(404)
        else:
            if amenity_id in place.amenity_ids:
                place.amenity_ids.remove(amenity_id)
            else:
                abort(404)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    strict_slashes=False, methods=["POST"]
)
def create_amenity_place(place_id, amenity_id):  # Links an amenity to a place
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place and not amenity:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity not in place.amenities:
            place.amenities.append(amenity)
        else:
            return make_response(jsonify(amenity.to_dict()), 200)
    else:
        if amenity_id not in place.amenity_ids:
            place.amenity_ids.append(amenity_id)
        else:
            return make_response(jsonify(amenity.to_dict()), 200)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
