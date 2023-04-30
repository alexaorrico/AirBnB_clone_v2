#!/usr/bin/python3

'''
Create a new view for Review objects that handles
all default RestFul API actions.
'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False,
                 methods=['GET'])
@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE', 'POST'])
def place_amenity_crud(place_id=None, amenity_id=None):
    '''Returns GET, DELETE, POST methods'''
    data = {
        "p_id": place_id,
        "a_id": amenity_id
    }
    methods = {
            'GET': get,
            'DELETE': delete,
            'POST': post,
            }
    if request.method in methods:
        return methods[request.method](data)


def get(data):
    '''Sends HTTP GET request'''
    found = storage.get("Place", data["p_id"])
    if not found:
        abort(404)
    return jsonify([x.to_dict() for x in found.amenities]), 200


def delete(data):
    '''Sends HTTP DELETE request'''
    found_place = storage.get("Place", data["p_id"])
    if not found_place:
        abort(404)
    found_amenity = storage.get("Amenity", data["a_id"])
    if not found_amenity:
        abort(404)
    if found_amenity not in found_place.amenities:
        abort(404)
    found_place.amenities.remove(found_amenity)
    storage.save()
    return jsonify({}), 200


def post(data):
    '''Sends HTTP POST request'''
    found_place = storage.get("Place", data["p_id"])
    if not found_place:
        abort(404)
    found_amenity = storage.get("Amenity", data["a_id"])
    if not found_amenity:
        abort(404)
    if found_amenity in found_place.amenities:
        return jsonify(found_amenity.to_dict()), 200
    else:
        found_place.amenities.append(found_amenity)
        storage.save()
        return jsonify(found_amenity.to_dict()), 201
