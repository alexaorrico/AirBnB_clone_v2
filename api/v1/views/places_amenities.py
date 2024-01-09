#!/usr/bin/python3
"""creates view for place objects and amenity
objects that handles all RESTFull API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def list_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        return jsonify([x.to_dict() for x in place.amenities])
    amenities = place.amenity_ids
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes a amenity to a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity_id not in [x.id for x in place.amenities]:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({})
    else:
        place.amenity_ids.pop(amenity_id, None)
        place.save()
        return jsonify({})


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    """links a Amenity object to a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity_id in [x.id for x in place.amenities]:
            return jsonify(amenity.to_dict())
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
