#!/usr/bin/python3
"""
Define route for view amenity
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.amenity import Amenity
from models import storage, storage_t


@app_views.route('/places/<string:place_id>/amenities', strict_slashes=False)
@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 strict_slashes=False, methods=['DELETE', 'POST'])
def amenities_place(place_id=None, amenity_id=None):
    """Retrieves amenity or All the amenities given place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if amenity_id is None:
        if storage_t == 'db':
            amenities = [amenity.to_dict() for amenity in place.amenities]
        else:
            amenities = [storage.get(Amenity, amenity_id)
                         for amenity_id in place.amenities]
        return jsonify(amenities)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'DELETE':
        if storage_t == 'db':
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
        else:
            if amenity_id not in place.amenities:
                abort(404)
            place.amenity_id.remove(amenity.id)
        storage.save()
        return jsonify({})

    if request.method == 'POST':
        if storage_t == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict())
            place.amenities.append(amenity)
        else:
            if amenity_id in place.amenities:
                return jsonify(amenity.to_dict())
            place.amenity_id.append(amenity.id)
        storage.save()
        return jsonify(amenity.to_dict()), 201
