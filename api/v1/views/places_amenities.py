#!/usr/bin/python3
"""Places Amenities API"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=['GET'])
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    found = None
    if storage_t == 'db':
        found = list(filter(lambda d: d.id == amenity_id, place.amenities))
    else:
        found = list(filter(lambda id: id == amenity_id, place.amenity_ids))
    if len(found) == 0:
        abort(404)
    if storage_t == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)
    place.save()
    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['POST'])
def link_amenity_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage_t == 'db':
        found = list(filter(lambda d: d.id == amenity_id, place.amenities))
    else:
        found = list(filter(lambda id: id == amenity_id, place.amenity_ids))

    if len(found) == 1:
        return jsonify(amenity.to_dict()), 200
    if storage_t == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)
    place.save()
    return jsonify(amenity.to_dict()), 201
