#!/usr/bin/python3
"""
Place - Amenity routes
"""

from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
from flask import jsonify, abort, request
from models.user import User
from os import getenv

STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<string:place_id>/amenities', methods=["GET"],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Get all amenities of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if place.amenities is None:
        abort(404)
    if STORAGE_TYPE == "db":
        amenities_list = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = place.amenities
        amenities_list = []
        for amenity in amenities:
            amenities_list.append(amenity.to_dict())
    return (jsonify(amenities_list))


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Delete amenity from a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if (amenity not in place.amenities and
       amenity.id not in place.amenities):
        abort(404)
    if STORAGE_TYPE == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return {}, 200


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=["POST"],
                 strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Link an amenity to a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if (amenity in place.amenities or
       amenity.id in place.amenities):
        return amenity.to_dict(), 200
    if STORAGE_TYPE == "db":
        place.amenities.append(amenity)
    else:
        place.amenities = amenity

    return amenity.to_dict(), 201
