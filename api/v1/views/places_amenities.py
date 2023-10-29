#!/usr/bin/python3

"""
a view for Place->Amenity relationship that handles all default RESTFul
API actions

Author: Khotso Selading and Londeka Dlamini
"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def place_amenity(place_id):
    """retrieves of a list of all place objects"""
    place_object = storage.get(Place, place_id)

    if not place_object:
        abort(404)

    return jsonify([obj.to_dict() for obj in place_object.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_place_amenity(place_id, amenity_id):
    """retrieves specific place obj"""
    place_object = storage.get(Place, place_id)

    if place_object is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place_object.amenities:
        abort(404)
    for i in range(len(place_object.amenities)):
        if place_object.amenities[i] == amenity:
            place_object.amenities[i].delete()
            storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """deletes specific place object"""
    place_object = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place_object is None:
        abort(404)

    if amenity is None:
        abort(404)
    if amenity in place_object.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)

    place_object.amenities.append(amenity)
    place_object.save()
    return make_response(jsonify(amenity.to_dict()), 201)
