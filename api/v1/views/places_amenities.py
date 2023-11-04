#!/usr/bin/python3
'''places.py'''
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_by_place(place_id=None):
    '''get amenities by places'''
    place = storage.get(Place, place_id)
    if place:
        amenities = []
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            amenities_obj = place.amenities
        else:
            amenities_obj = place.amenity_ids

        for amenity in amenities_obj:
            amenities.append(amenity.to_dict())
        return jsonify(amenities)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_aminities_by_place(place_id=None, amenity_id=None):
    '''delete place'''
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                if amenity not in place.amenities:
                    abort(404)
            else:
                if amenity.id not in place.amenity_ids:
                    abort(404)
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """adds an amenity object to a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return jsonify(amenity.to_dict())
    place_amenities.append(amenity)
    place.save()
    return jsonify(amenityto_dict()), 201
