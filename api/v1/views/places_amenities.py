#!/usr/bin/python3
'''Contains the places_amenities view for the API.'''
from flask import abort, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models import amenity
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    obj_place = storage.get(Place, place_id)
    if not obj_place:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        obj = [amenity.to_dict() for amenity in obj_place.amenities]
    else:
        obj = [storage.get(Amenity, amenity_id).to_dict()
               for amenity_id in obj_place.amenity_ids]
    return jsonify(obj)


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
