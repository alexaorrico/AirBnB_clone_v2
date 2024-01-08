#!/usr/bin/python3
""" Place Amenity views for modules"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id):
    """lists all Amenity objects based on the place_id"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity_list = []
    storage_type = getenv("HBNB_TYPE_STORAGE")
    if storage_type == 'db':
        for amenity in place.amenities:
            amenity_list.append(amenity.to_dict())
    else:
        for amenity_id in place.amenity_ids:
            amenity_list.append(storage.get(Amenity, amenity_id).to_dict())
    return jsonify(amenity_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object to a Place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage_type = getenv("HBNB_TYPE_STORAGE")
    if storage_type == 'db':
        if amenity not in place.amenities:
            abort(404)
        else:
            place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        else:
            place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def add_place_amenity(place_id, amenity_id):
    """Adds a place amenity"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage_type = getenv("HBNB_TYPE_STORAGE")
    if storage_type == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
