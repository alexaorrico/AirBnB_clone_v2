#!/usr/bin/python3
"""Create a view for the link for Place & Amenity"""

from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import environ


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object from a place"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Links an amenity object to a place"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
