#!/usr/bin/python3
""" New view for link between place objects and amenity objects """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
import models


@app_views.route('/places/<place_id>/amenities/', methods=['GET'])
@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def all_places_amenities(place_id):
    """ gets amenity objects by place_id """
    json_list = []
    try:
        amenity_list = storage.get('Place', place_id).amenities
        for amenity in amenity_list:
            json_list.append(amenity.to_dict())
        return jsonify(json_list)
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """ Deletes place amenity """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    else:
        place.amenities.remove(amenity)
        place.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    """ links amenity and place """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
