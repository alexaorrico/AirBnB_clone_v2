#!/usr/bin/python3
"""view for Amenity objects that handles all default RestFul API actions:"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel


@app_views.route("/places/<place_id>/amenities/",
                 methods=['GET'], strict_slashes=False)
def all_amenities_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    amenities = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = place.amenities
    for val in amenity:
        amenities.append(val.to_dict())
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def del_amenities_place(place_id, amenity_id):
    """Deletes an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity_id not in [ameni.id for ameni in place.amenities]:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity_id in [ameni.id for ameni in place.amenities]:
        return jsonify(amenity.to_dict()), 200
    else:
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
