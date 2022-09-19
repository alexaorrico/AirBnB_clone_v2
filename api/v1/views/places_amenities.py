#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def places_amenities_get(place_id):
    """Retrieves the list of all Place & Amenities"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)

    all_amenities = []
    for amenity in place.amenities:
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def places_amenities_id_delete(place_id, amenity_id):
    """Deletes Place & Amenity object and 404 if it's an error"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def places_amenities_id_put(place_id, amenity_id):
    """Updates Place & Amenity object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    amenity.save()
    return jsonify(amenity.to_dict()), 201
