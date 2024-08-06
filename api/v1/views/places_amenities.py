#!/usr/bin/python3
"""
all default RESTFul API actions
for Place-Amenity obj
"""

from os import environ
from flask import abort, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route(
    "/places/<place_id>/amenities", methods=["GET"], strict_slashes=False
)
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity obje"""
    # check if place exists
    place_d_a = storage.get(Place, place_id)
    if place_d_a is None:
        abort(404)

    if environ.get("HBNB_TYPE_STORAGE") == "db":
        amen_d = [obj.to_dict() for obj in place_d_a.amenities]
    else:  # file storage
        amen_d = [
            storage.get(Amenity, amenity_id).to_dict()
            for amenity_id in place_d_a.amenity_ids
        ]
    return jsonify(amen_d)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_place_amenity(place_id, amenity_id):
    """Retrieves the list all obj"""

    place_d_a = storage.get(Place, place_id)
    if place_d_a is None:
        abort(404)

    amen_a = storage.get(Amenity, amenity_id)
    if amen_a is None:
        abort(404)

    if environ.get("HBNB_TYPE_STORAGE") == "db":
        if amen_a not in place_d_a.amenities:
            abort(404)
        place_d_a.amenities.remove(amen_a)
    else:
        if amenity_id not in place_d_a.amenity_ids:
            abort(404)
        place_d_a.amenity_ids.remove(amenity_id)

    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["POST"],
    strict_slashes=False,
)
def post_place_amenity(place_id, amenity_id):
    """Link  Amenity obj"""
    plac_a = storage.get(Place, place_id)
    if plac_a is None:
        abort(404)

    amen_d = storage.get(Amenity, amenity_id)
    if amen_d is None:
        abort(404)

    if environ.get("HBNB_TYPE_STORAGE") == "db":
        if amen_d in plac_a.amenities:
            return make_response(jsonify(amen_d.to_dict()), 200)
        else:
            plac_a.amenities.append(amen_d)
    else:
        if amenity_id in plac_a.amenity_ids:
            return make_response(jsonify(amen_d.to_dict()), 200)
        else:
            plac_a.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amen_d.to_dict()), 201)
