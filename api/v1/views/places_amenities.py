#!/usr/bin/python3
"""
Place amenities API routes
"""
from flask import jsonify, abort

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Returns a list of all amenities available in a given place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """"Unlinks amenity from a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity or all(am.id != amenity_id for am in place.amenities):
        abort(404)
    place.amenities = [am for am in place.amenities if am.id != amenity_id]
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Links amenity to a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if any(am.id == amenity_id for am in place.amenities):
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
