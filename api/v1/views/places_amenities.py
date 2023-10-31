#!/usr/bin/python3
"""A script that handles api between places and amenity"""
from flask import jsonify
from flask import abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity


@app_views.route('places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def getPlaceAmenity(place_id):
    """To GET place amenity using place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def ToDeleteAmenity(place_id, amenity_id):
    """To delete amenity objects"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    if amenity_obj not in place_obj.amenities:
        abort(404)

    place_obj.amenities.remove(amenity_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def ToPostAmenity(place_id, amenity_id):
    """To check if the place_id and amenity_id is linked,
    then create an object"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    if amenity_obj in place_obj.amenities:
        return jsonify(amenity_obj.to_dict()), 200

    place_obj.amenities.append(amenity_obj)
    storage.save()

    return jsonify(amenity_obj.to_dict()), 201
