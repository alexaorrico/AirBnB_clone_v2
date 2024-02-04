#!/usr/bin/python3
"""
Module to handle the link between Place objects and Amenity objects for the RESTful API
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET', 'POST'])
def places_amenities(place_id):
    """
    Handles GET and POST requests on /places/<place_id>/amenities route
    """

    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    if request.method == 'GET':
        amenities_list = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities_list)

    elif request.method == 'POST':
        amenity_id = request.args.get('amenity_id')

        if amenity_id is None:
            abort(404)

        amenity = storage.get("Amenity", amenity_id)

        if amenity is None:
            abort(404)

        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_places_amenity(place_id, amenity_id):
    """
    Handles DELETE requests on /places/<place_id>/amenities/<amenity_id> route
    """

    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200
