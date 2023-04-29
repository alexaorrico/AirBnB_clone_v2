#!/usr/bin/python3
"""
This view implements the RESTful action for the link between
`Place` and `Amenity` objects
"""

from models import storage_t, storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort, make_response
from . import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def read_place_amenities(place_id):
    """
    Retrieves list of all `Amenity` objects associated with a given `place_id`
    """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify([
        amenity.to_dict() for amenity in place.amenities
    ])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Deletes an `Amenity` object from a given `place_id`"""

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if storage_t != "db":
        place.amenity_ids.remove(amenity.id)
    else:
        place.amenities.remove(amenity)
    place.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def create_place_amenity(place_id, amenity_id):
    """Creates an `Amenity` object from a given `place_id`"""

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)

    if storage_t != "db":
        place.amenity_ids.append(amenity.id)
    else:
        place.amenities.append(amenity)
    place.save()

    return make_response(jsonify(amenity.to_dict()), 201)
