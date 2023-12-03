#!/usr/bin/python3
"""Place_amenity module"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.amenity import Amenity
from models.place import Place
from flasgger.utils import swag_from


# GET
@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/get_id.yml', methods=['GET'])
def get_place_amenities(place_id):
    """Retrieves all Place_amenity objects from a place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    amenities = [obj.to_dict() for obj in place.amenities]
    return jsonify(amenities)


# DELETE
@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place_amenity/delete.yml', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Deletes Place_amenity object from place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({})


# POST
@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
@swag_from('documentation/place_amenity/post.yml', methods=['POST'])
def create_place_amenity(place_id, amenity_id):
    """Create Place_amenity object"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return (jsonify(amenity.to_dict()), 200)

    place.amenities.append(amenity)
    storage.save()
    return (jsonify(amenity.to_dict()), 201)
