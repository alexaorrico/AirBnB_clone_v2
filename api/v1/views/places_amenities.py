#!/usr/bin/python3
"""
Places_Amenities Module
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage, Place, Amenity
from models.place import Place
from models.amenity import Amenity

# Import the CORS class if needed

# CORS(app_views, resources={r"/*": {"origins": "0.0.0.0"}})


@app_views.route('/places/<place_id>/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_amenities(place_id):
    """Retrieve the list of all Amenity objects of a Place
    or link a Amenity object to a Place"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    if request.method == 'GET':
        amenities_list = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities_list)

    elif request.method == 'POST':
        amenity_id = request.args.get('amenity_id')
        amenity = storage.get("Amenity", amenity_id)

        if amenity is None:
            abort(404)

        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        storage.save()

        return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_places_amenities(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()

    return jsonify({}), 200
