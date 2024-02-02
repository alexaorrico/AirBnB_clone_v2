#!/usr/bin/python3
'''View to handle the RESTful API actions for 'User' objects'''
from flask import jsonify, request, abort

from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage, storage_t


@app_views.route('/places/<string:place_id>/amenities', strict_slashes=False)
def place_amenities(place_id):
    '''Handles "/places/<place_id>/amenities" route'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if storage_t == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, id).to_dict()
                     for id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST', 'DELETE'], strict_slashes=False)
def places_amenity_actions(place_id, amenity_id):
    '''Handles actions for "/places/<place_id>/amenities/<amenity_id>" route'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'DELETE':
        if storage_t == 'db':
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.remove(amenity_id)
        storage.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if storage_t == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenities.append(amenity)
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.append(amenity_id)
        storage.save()
        return jsonify(amenity.to_dict()), 201
