#!/usr/bin/python3
"""

Flask web server creation to handle api petition-requests

"""
from flask import jsonify, abort
from flask import request
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def all_amenities_place(place_id):
    """
    Retrieves the list of all Amenity objects
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)
    my_list = []
    for amenity in place.amenities:
        my_list.append(amenity.to_dict())
    return jsonify(my_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_amenity_place(place_id, amenity_id):
    """
    Deletes an Amenity object if id is linked to Place and Amenity object
    """
    place_objs = storage.get(classes["Place"], place_id)
    if place_objs is None:
        abort(404)
    amenity_objs = storage.get(classes["Amenity"], amenity_id)
    if amenity_objs is None:
        abort(404)
    if amenity_objs not in place_objs.amenities:
        abort(404)
    storage.delete(amenity_objs)
    storage.save()
    return jsonify({})


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def post_amenity_place(place_id, amenity_id):
    """
    Link a Amenity object to a Place
    """
    place_objs = storage.get(classes["Place"], place_id)
    if place_objs is None:
        abort(404)
    amenity_objs = storage.get(classes["Amenity"], amenity_id)
    if amenity_objs is None:
        abort(404)
    if amenity_objs in place_objs.amenities:
        return jsonify(amenity_objs.to_dict())
    return jsonify(amenity_objs.to_dict()), 201
