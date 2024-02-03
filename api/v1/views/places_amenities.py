#!/usr/bin/python3

"""
A view for Place objects that handles all default RESTFul API Actions
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from models.place import Place
import os


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def amenities_by_place(place_id):
    """Retrieves and posts amenities by place_id."""
    # Retrieve the Place object with the given place_id
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities_list = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST', 'DELETE'])
def amenity_of_place(place_id, amenity_id):
    """ Function for linking amenity to place, or deleting link """
    # Retrieve the Place object with the given place_id
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    # Handling DELETE and POST for FileStorage
    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        if request.method == 'POST':
            amenities_ids = place.amenity_ids
            for am_id in amenities_ids:
                if am_id == amenity_id:
                    return jsonify(amenity.to_dict()), 200
            place.amenity_ids.append(amenity.id)
            storage.save()
            return jsonify(amenity.to_dict()), 201
        if request.method == 'DELETE':
            amenities_ids = place.amenity_ids
            for am_id in amenities_ids:
                if am_id == amenity_id:
                    place.amenity_ids.remove(amenity.id)
                    storage.save()
                    return jsonify({}), 200
            abort(404)
    # Handling DELETE and POST methods for dbStorage
    else:
        if request.method == 'POST':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenities.append(amenity)
            storage.save()
            return (amenity.to_dict()), 201
        else:
            if amenity not in place.amenities:
                abort(404)
            else:
                place.amenities.remove(amenity)
                storage.save()
                return jsonify({}), 200
