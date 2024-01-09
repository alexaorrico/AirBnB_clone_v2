#!/usr/bin/python3
"""
Defines the RESTful API actions for the link
between Place objects and Amenity objects.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET', 'POST'])
def places_amenities(place_id):
    """
    Handles default RESTful API actions for
    the link between Place and Amenity
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if request.method == 'GET':
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)

    if request.method == 'POST':
        amenity_id = request.get_json().get('amenity_id')
        amenity = storage.get(Amenity, amenity_id)

        if amenity is None:
            abort(404)

        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def unlink_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object from a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None or amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200
