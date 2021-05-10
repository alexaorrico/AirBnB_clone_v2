#!/usr/bin/python3
""" Places amenities """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenities import Amenities
from models.place import Place
import os


@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def all_amenities(place_id):
    """ Retrieve all amenities """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities_info = place.amenities
    else:
        amenities_info = place.amenities_ids
    for data in amenities_info:
        amenities.append(data.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id', methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """ Detelete amenity """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None:
        abort(404)
    if amenity_id is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        abort(404)
    place_amenities.remove(amenity)
    place.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """adds an amenity object to a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return jsonify(amenity.to_dict())
    place_amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenityto_dict()), 201)
