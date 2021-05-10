#!/usr/bin/python3
"""
    This is the places amenities page handler for Flask.
"""
from api.v1.views.places import places_id
from api.v1.views import app_views
from api.v1 import *
from models import storage
from flask import abort, jsonify, request

from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity


@app_views.route('/places/<id>/amenities', methods=['GET'])
def places_id_amenities(id):
    """
        Flask route at /places/<id>/amenities.
    """
    place = storage.get(Place, id)
    if (place):
        if storage_t == 'db':
            return jsonify([r.to_dict() for r in place.amenities])
        elif storage_t == 'fs':
            return jsonify(place.to_dict()["amenity_ids"])
    abort(404)


@app_views.route('/places/<id>/amenities/<am_id>', methods=['DELETE', 'POST'])
def places_id_amenities_id(id, am_id):
    """
        Flask route at /places/<id>/amenities/<am_id>.
    """
    place = storage.get(Place, id)
    if (place):
        if request.method == 'DELETE':
            amenity = storage.get(Amenity, am_id)
            if (amenity):
                if storage_t == 'db':
                    if (amenity in place.amenities):
                        place.amenities.remove(amenity)
                        storage.save()
                        return {}, 200
                    abort(404)
                elif storage_t == 'fs':
                    if (am_id in place.amenity_ids):
                        place.amenity_ids.remove(am_id)
                        storage.save()
                        return {}, 200
                    abort(404)
            abort(404)
        elif request.method == 'POST':
            amenity = storage.get(Amenity, am_id)
            place = storage.get(Place, id)
            if (place):
                if (amenity):
                    if storage_t == 'db':
                        if (amenity not in place.amenities):
                            place.amenities.append(amenity)
                            storage.save()
                            return amenity.to_dict(), 201
                    elif storage_t == 'fs':
                        if (am_id not in place.amenity_ids):
                            place.amenity_ids.append(am_id)
                            storage.save()
                            return amenity.to_dict(), 200
                    abort(404)
                abort(404)
            abort(404)
    abort(404)
