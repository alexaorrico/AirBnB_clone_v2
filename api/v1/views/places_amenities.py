#!/usr/bin/python3
"""Creates a new view for the link between Place
objects and Amenity objects that handles all default
RESTFul API actions"""
from models.place import Place
from models.amenity import Amenity
from flask import request, abort, jsonify
from models import storage
from api.v1.views import app_views
from os import environ

@app_views.route('/places/<string:place_id>/amenities', strict_slashes=False,
        methods=['GET'])
def get_all_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    all_amenities = []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]

    return jsonify(amenities)
