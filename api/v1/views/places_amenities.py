#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views

app = Flask(__name__)


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenity_for_place(place_id=None):
    """Retrieves the list of all Amenity objects for a place"""
    place_object = storage.get("Place", place_id)
    if place_object is None:
        return jsonify({}), 404
    amenities_list = []
    for amenity in place_object.amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_to_place(place_id=None, amenity_id=None):
    """Deletes a Amenity object"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    if amenity_obj not in place_obj.amenities:
        abort(404)
    else:
        storage.delete(amenity_obj)
        storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_amenity_to_place(place_id=None, amenity_id=None):
    """Links an Amenity object to a Place"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    amenity_ids = []
    for amenity in place_obj.amenities:
        if amenity.id == amenity_obj.id:
            return jsonify(amenity_obj.to_dict()), 200
    place_obj.amenities.append(amenity_obj)
    storage.save()
    return jsonify(amenity_obj.to_dict()), 201
