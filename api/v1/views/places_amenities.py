#!/usr/bin/python3
"""This the view for API request concerning the places and amenities
"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'POST'],
                 strict_slashes=False)
def place_amenity_requests(place_id=None, amenity_id=None):
    """This method serves API request to Places/Amenities
    """
    mode = getenv('HBNB_TYPE_STORAGE')

    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)

        amenity_list = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenity_list)
    elif request.method == 'DELETE':
        place = storage.get(Place, place_id)
        amenity = storage.get(Amenity, amenity_id)
        if place is None or amenity is None:
            abort(404)
        if amenity not in place.amenities:
            abort(404)

        if mode != 'db':
            place.amenity_ids.remove('Amenity.' + amenity_id)

        storage.delete(amenity)
        storage.save()

        return jsonify({}), 200
    elif request.method == 'POST':
        place = storage.get(Place, place_id)
        amenity = storage.get(Amenity, amenity_id)
        if place is None or amenity is None:
            abort(404)

        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        if mode == 'db':
            place.amenities.append(amenity)

        else:
            place.amenity_ids.append('Amenity.' + amenity_id)

        storage.save()
        return jsonify(amenity.to_dict()), 201

    else:
        abort(501)
