#!/usr/bin/python3
""" Places """
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=["GET"],
                 strict_slashes=False)
def place_amenities(place_id):
    """ Place amenities' list """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        amenities_dict = []
        for amenity in place.amenities:
            amenities_dict.append(amenity.to_dict())
        return jsonify(amenities_dict), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=["DELETE", "POST"], strict_slashes=False)
def place_amenity(place_id, amenity_id):
    """ Place_amenity """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "DELETE":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200
    if request.method == "POST":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
