#!/usr/bin/python3
"""
Api views for place amenities
"""
from models.amenity import Amenity
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
import os


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id):
    """
    Retrieves the list of
    all Amenity objects of a Place
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenities = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        objs = place.amenities
    else:
        objs = place.amenity_ids
    for amenity in objs:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place
    """
    amenity = storage.get("Amenity", amenity_id)
    place = storage.get("Place", place_id)
    if not place or not amenity:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        objs = place.amenities
    else:
        objs = place.amenity_ids
    if amenity not in objs:
        abort(404)
    objs.remove(amenity)
    place.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
    Link a Amenity object to a Place
    """
    amenity = storage.get("Amenity", amenity_id)
    place = storage.get("Place", place_id)
    if not amenity or not place:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        objs = place.amenities
    else:
        objs = place.amenity_ids
    if amenity in objs:
        return jsonify(amenity.to_dict())
    objs.append(amenity)
    place.save()
    return make_response(jsonify(amenityto_dict()), 201)
