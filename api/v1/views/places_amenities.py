#!/usr/bin/python3
"""Define Place Amenities Routes"""
from os import getenv
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def place_amenities(place_id):
    """Defines places/<place_id>/amenities/<amenity_id> with GET method

    GET - Get all Amenities related to a given place_id
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    # GET
    if request.method == "GET":
        return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST", "DELETE"])
def place_amenity(place_id, amenity_id):
    """Define places/<place_id>/amenities/<amenity_id>
    with POST and DELETE methods

    DELETE - Deletes a Review  with the given id
    POST - link an amenity to a place
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)

    already_exist = False
    # POST
    if request.method == "POST":
        if getenv("HBNB_TYPE_STORAGE", None) == "db":
            # Storage type db
            if amenity not in place.amenities:
                place.amenities.append(amenity)
            else:
                already_exist = True
        else:
            # Storgae type file
            if amenity.id not in place.amenity_ids:
                place.amenity_ids.append(amenity_id)
            else:
                already_exist = True
        place.save()
        return jsonify(amenity.to_dict()), (201 if not already_exist else 200)

    # DELETE
    if getenv("HBNB_TYPE_STORAGE", None) == "db":
        # Storage type db
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        # Storgae type file
        if amenity.id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    place.save()
    return jsonify({})
