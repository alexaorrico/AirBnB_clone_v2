#!/usr/bin/python3
"""endpoints for places review"""
from os import environ
from models import storage
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def all_place_amenity(place_id):
    """gets all amenities"""
    d_place = storage.get(Place, place_id)

    if not d_place:
        abort(404)

    if environ.get("HBNB_TYPE_STORAGE") == "db":
        d_amen = [am.to_dict() for am in d_place.amenities]
    else:
        d_amen = [storage.get(Amenity, am_id).to_dict()
                  for am_id in d_place.amenity_ids]

    return jsonify(d_amen)


@app_views.route("/places/<place_id>/amenites/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def kill_place(place_id, amenity_id):
    """deletes places with id supplied"""
    d_place = storage.get(Place, place_id)

    if not d_place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if environ.get("HBNB_TYPE_STORAGE") == "db":
        if amenity not in d_place.amenities:
            abort(404)
        d_place.amenities.remove(amenity)
    else:
        if amenity_id not in d_place.amenity_ids:
            abort(404)
        d_place.amenity_ids.remove(amenity_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    """this endpoints creates new amenities"""
    d_place = storage.get(Place, place_id)

    if not d_place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if environ.get("HBNB_TYPE_STORAGE") == "db":
        if amenity in d_place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            d_place.amenities.append(amenity)
    else:
        if amenity_id in d_place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            d_place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
