#!/usr/bin/python3
"""
view for the link between Place objects and Amenity objects that handles
all default RestFul API actions
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def handle_places_amenities(place_id, amenity_id=None):
    """
    Retrieves the list of all Amenity objects of a Place,
    delete or create an Amenity object of a Place
    """
    place_obj = storage.get("Place", place_id)
    if place_obj:
        if request.method == 'GET' and amenity_id is None:
            return jsonify([amenity_obj.to_dict() for amenity_obj in place_obj.
                            amenities]), 200
        amenity_ids = [amenity_obj.id for amenity_obj in place_obj.amenities]
        amenity_obj = storage.get("Amenity", amenity_id)
        if amenity_obj:
            if request.method == 'DELETE':
                if amenity_id not in amenity_ids:
                    abort(404)
                place_obj.amenities.remove(amenity_obj)
                storage.save()
                return {}, 200
            if request.method == 'POST':
                if amenity_id in amenity_ids:
                    return jsonify(amenity_obj.to_dict()), 200
                # kwargs = request.get_json(silent=True)
                # if kwargs:
                #     for k, v in kwargs.items():
                #         setattr(amenity_obj, k, v)
                place_obj.amenities.append(amenity_obj)
                place_obj.save()
                return jsonify(amenity_obj.to_dict()), 201
        else:
            abort(404)
    else:
        abort(404)
