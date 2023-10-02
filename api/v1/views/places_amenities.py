#!/usr/bin/python3
"""
    API module places_amenitiess
"""

import models
from models import storage
from models.place import *
from models.user import *
from models.amenity import *

from flask import jsonify, abort, request, make_response
from os import environ as env
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """
        A function that Retrieves the list of all Amenity
        objects of a Place: GET /api/v1/places/<place_id>/amenities
    """
    # get place by id
    place = storage.get(Place, place_id)

    if (place):
        # get environment type then process amenity
        if (env.get('HBNB_TYPE_STORAGE') == 'db'):
            amenityList = [amenity.to_dict() for amenity in place.amenities]
        else:
            amenityList = [storage.get(Amenity, amenityID).to_dict()
                        for amenityID in place.amenity_ids]

        return jsonify(amenityList)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                  methods=['DELETE'], strict_slashes=False)
def del_place_amenity(place_id, amenity_id):
    """
        A function that Deletes a Amenity object to a Place:
        DELETE /api/v1/places/<place_id>/amenities/<amenity_id>
    """
    # get place by id
    place = storage.get(Place, place_id)
    if (not place):
        abort(404)

     # get amenities by id
    amenity = storage.get(Amenity, amenity_id)

    if (amenity):
        # get environment type then delete place amenity
        if (env.get('HBNB_TYPE_STORAGE') == 'db'):
            if (amenity in place.amenities):
                place.amenities.remove(amenity)
            else:
                abort(404)
        else:
            if (amenity_id in place.amenity_ids):
                place.amenity_ids.remove(amenity_id)
            else:
                abort(404)

        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                  methods=['POST'], strict_slashes=False)
def add_place_amenity(place_id, amenity_id):
    """
        A function that Link a Amenity object to a Place:
        POST /api/v1/places/<place_id>/amenities/<amenity_id>
    """
    # get place by id
    place = storage.get(Place, place_id)
    if (not place):
        abort(404)

     # get amenities by id
    amenity = storage.get(Amenity, amenity_id)

    if (amenity):
        # get environment type then add place amenity
        if (env.get('HBNB_TYPE_STORAGE') == 'db'):
            if (amenity in place.amenities):
                return make_response(jsonify(amenity.to_dict()), 200)
            else:
                place.amenities.append(amenity)
        else:
            if (amenity_id in place.amenity_ids):
                return make_response(jsonify(amenity.to_dict()), 200)
            else:
                place.amenity_ids.append(amenity_id)

        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)
    else:
        abort(404)
