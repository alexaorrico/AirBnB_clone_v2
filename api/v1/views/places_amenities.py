#!/usr/bin/python3
"""View for API request concerning the place/amenity relationship
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
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
    """Methods serving API requests for place/amenity
    relationships
    """
    mode = getenv('HBNB_TYPE_STORAGE')

    # GET REQUESTS
    if request.method == 'GET':
        # fetch place object
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)

        amenity_list = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenity_list)

    # DELETE REQUESTS
    elif request.method == 'DELETE':
        # validate place and amenity objects
        place = storage.get(Place, place_id)
        amenity = storage.get(Amenity, amenity_id)
        if place is None or amenity is None:
            abort(404)

        if amenity not in place.amenities:
            abort(404)

        if mode != 'db':  # FileStorage mode
            place.amenity_ids.remove('Amenity.' + amenity_id)

        storage.delete(amenity)
        storage.save()

        return jsonify({}), 200

    # POST REQUESTS
    elif request.method == 'POST':
        # link amenity to place
        place = storage.get(Place, place_id)
        amenity = storage.get(Amenity, amenity_id)
        if place is None or amenity is None:
            abort(404)

        # if relationship already exists
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        if mode == 'db':  # DBStorage mode
            place.amenities.append(amenity)

        else:  # FileStorage mode
            place.amenity_ids.append('Amenity.' + amenity_id)

        storage.save()
        return jsonify(amenity.to_dict()), 201

    # UNSUPPORTED REQUESTS
    else:
        abort(501)
