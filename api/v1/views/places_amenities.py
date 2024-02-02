#!/usr/bin/python3

"""
A view for Amenity objects that handles all default RESTFul API Actions
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity



@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET', 'POST'])
def places_amenities(place_id, amenity_id):
    """
    Retrieves amenities associated with a place or associates a new amenity with a place.
    """
    # Retrieve the Place object with the given place_id
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    # Action for GET method
    if request.method == 'GET':
        amenities_list = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities_list)

    # Action for POST method
    if request.method == 'POST':
        amenity_id = request.args.get('amenity_id')
        if amenity_id is None:
            abort(404)
        # Retrieve the Amenity object with the given amenity_id
        amenity = storage.get(Amenity, amenity_id)

        if amenity is None:
            abort(404)

        # If amenity is already associated with the place, return it with status code 200
        if storage_t == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenities.append(amenity)
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.append(amenity)

        # Associate the amenity with the place, save, and return with status code 201
        storage.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes the association of an amenity with a place.
    """
    # Retrieve the Place object with the given place_id
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    # Retrieve the Amenity object with the given amenity_id
    amenity = storage.get(Amenity, amenity_id)

    # Check if the amenity exists and is associated with the place
    if amenity is None or amenity not in place.amenities:
        abort(404)

    # Remove the amenity from the place's amenities, save, and return with status code 200
    if storage_t == 'db':
        place.amenities.delete(amenity)
    else:
        place.amenity_ids.remove(amenity_id)
    storage.save()
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200
