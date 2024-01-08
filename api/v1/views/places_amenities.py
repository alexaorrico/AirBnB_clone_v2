#!/usr/bin/python3
"""
contains endpoints(routes) for place_amenities objects
"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<string:place_id>/amenities", strict_slashes=False)
def get_amenities(place_id):
    """
    Retrieves the list of all amenities objects of a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_objects = place.amenities
    else:
        amenity_objects = place.amenity_ids
    amenities = [obj.to_dict() for obj in place.amenities]
    return jsonify(amenities)


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def del_amenity(place_id, amenity_id):
    """
    Deletes a amenity object from place
    """

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 strict_slashes=False, methods=['POST'])
def create_amenity2(place_id, amenity_id):
    """
    Creates a new amenity instance and associates it with the place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)

    new_amenity = Amenity(name=amenity.name)
    place.amenities.append(new_amenity)
    storage.save()

    return make_response(jsonify(new_amenity.to_dict()), 201)
