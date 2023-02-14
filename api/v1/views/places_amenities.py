#!/usr/bin/python3
"""Places Amenities API"""
from models import storage
from models.place import Place
from models.amenity import Amenity
from . import app_views
from flask import jsonify, abort

@app_views.route("/places/<place_id>/amenities")
def place_amenities(place_id):
    """Get amenities of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = place.amenities
    amenity_list = []
    for amenity in amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)

@app_views.route("/places/<place_id>/amenities/<amenity_id>")
def delete_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})

@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def link_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if storage.get(Place, amenity.place_id):
        return jsonify(amenity.to_dict())
    amenity.place_id = place_id
    amenity.save()
    return jsonify(amenity.to_dict()), 201
