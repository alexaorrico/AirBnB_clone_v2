#!/usr/bin/python3

"""
Create a new view for the link between Place objects and
Amenity objects that handles
all default RestFul API actions.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amen(place_id):
    """ Return all amenities """
    place = storage.get(Place, place_id)
    if not place:
        abort(404, "Not found")
    if storage_t == "db":
        return jsonify([e.to_dict() for e in place.amenities])
    else:
        return jsonify([e.to_dict() for e in place.amenities_ids])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amen(place_id, amenity_id):
    """ Delete an amenity """
    pl = storage.get(Place, place_id)
    amn = storage.get(Amenity, amenity_id)
    if not pl or not amn:
        abort(404)
    if amn not in place.amenities:
        abort(404)
    if storage_t == "db":
        place.amenities.remove(amn)
    else:
        place.amenity_id.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_amen(place_id, amenity_id):
    """ Link an amenity to a place """
    place = storage.get(Place, place_id)
    amn = storage.get(Amenity, amenity_id)
    if not place or not amn:
        abort(404, "Not found")
    if amn in place.amenities:
        return jsonify(amenity.to_dict()), 200
    if storage_t == "db":
        place.amenities.append(amn)
        place.save()
    else:
        place.amenities_ids.append(amn)
        place.save()
    return jsonify(amn.to_dict()), 201
