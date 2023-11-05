#!/usr/bin/python3
'''places.py'''
from flask import abort, jsonify, make_response
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
def del_place_amenity(place_id, amenity_id):
    """Returns an empty dictionary with the status code 200"""
    obj_place = storage.get(Place, place_id)
    if not obj_place:
        abort(404)

    obj_amenity = storage.get(Amenity, amenity_id)
    if not obj_amenity:
        abort(404)

    for elem in obj_place.amenities:
        if elem.id == obj_amenity.id:
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                obj_place.amenities.remove(obj_amenity)
            else:
                obj_place.amenity_ids.remove(obj_amenity)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Returns the Amenity with the status code 201"""
    obj_place = storage.get(Place, place_id)
    if not obj_place:
        abort(404)

    obj_amenity = storage.get(Amenity, amenity_id)
    if not obj_amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if obj_amenity in obj_place.amenities:
            return make_response(jsonify(obj_amenity.to_dict()), 200)
        obj_place.amenities.append(obj_amenity)
    else:
        if amenity_id in obj_place.amenity_ids:
            return make_response(jsonify(obj_amenity.to_dict()), 200)
        obj_place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(obj_amenity.to_dict()), 201)
