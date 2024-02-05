#!/usr/bin/python3
"""Review objects view"""

import os
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.user import User



db_mode = os.getenv("HBNB_TYPE_STORAGE")


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenties_by_place(place_id):
    """Retrieves the list of all amenity objects of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenties(amenities_id):
    """Retrives a Amenties object"""
    amenities = storage.get(Amenity, amenities_id)
    if not amenities:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(place_id, amenity_id):
    """deleye an amenity my id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if db_mode == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenities_id

    for amenity in place_amenities:
        if amenity.id == amenity_id:
            amenity.delete()
            amenity.save()
        else:
            abort(404)
    return jsonify({}, 200)


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["POST"])
def link_amenity(place_id, amenity_id):
    """Link Amenity to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if db_mode == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenities_id

    if amenity not in place_amenities:
        place_amenities.append(amenity)
    else:
        return jsonify(amenity, 200)
