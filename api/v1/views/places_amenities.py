#!/usr/bin/python3
""" Python script new view for the link between
Place objects and Amenity objects that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def retrieve_place_amenity(place_id):
    """Defines the GET method that Retrieves
    the list of all Amenity objects of a Place.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify([a.to_dict() for a in place.amenities])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE", "POST"])
def delete_place_amenity(place_id, amenity_id):
    """Defines the DELETE method that Deletes a Amenity object to a Place.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == "POST":
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)

        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    elif request.method == "DELETE":

        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)

        if amenity not in place.amenities:
            abort(404)

        place.amenities.remove(amenity)
        storage.save()

        return jsonify({}), 200
