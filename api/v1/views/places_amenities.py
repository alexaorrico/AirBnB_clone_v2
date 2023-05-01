#!/usr/bin/python3
""" Flask views for the Places resource """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def get_place_amenities(place_id):
    """ An endpoint that returns all amenities of a place """
    rlist = []
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenities = place.amenities
    for amenity in amenities:
        rlist.append(amenity.to_dict())
    return jsonify(rlist)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """ An endpoint that deletes a specific amenity """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if amenity_id not in [a.id for a in place.amenities]:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
def create_place_amenity(place_id, amenity_id):
    """ An endpoint that creates a new amenity """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if amenity_id in [a.id for a in place.amenities]:
        return jsonify(amenity.to_dict()), 200
    else:
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
