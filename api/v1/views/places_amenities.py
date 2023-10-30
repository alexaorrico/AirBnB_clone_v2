#!/usr/bin/python3
"""handles all default RESTful API actions for places and amenity objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.user import User
from os import getenv


@app_views.route(
    '/places/<place_id>/amenities', methods=['GET'], strict_slashes=False
)
def get_amenities_objs(place_id):
    '''Retrieves the list of all Amenity objects of a Place'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        place_amenities = place.amenity_ids
    res = jsonify(place_amenities)
    res.status_code = 200
    return res


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE'], strict_slashes=False
)
def delete_amenity_from_place(place_id, amenity_id):
    '''Deletes a Amenity object from a Place'''
    linked = False
    place_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)
    if place_obj is None or amenity_obj is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = place_obj.amenities
        for amenity in amenities:
            if amenity.id == amenity_id:
                place_obj.amenities.remove(amenity)
                linked = True
                break
    else:
        amenities = place_obj.amenity_ids
        for amenity in amenities:
            if amenity == amenity_id:
                place_obj.amenity_ids.remove(amenity)
                linked = True
                break
    place_obj.save()
    if not linked:
        abort(404)
    res = jsonify({})
    res.status_code = 200
    return res


@app_views.route(
    '/places/<place_id>/amenities/link', methods=['POST'], strict_slashes=False
)
def link_amenity_to_place(place_id, amenity_id):
    '''Link an Amenity object to a Place'''
    linked = None
    place_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)
    if place_obj is None or amenity_obj is None:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        for amenity in place_obj.amenities:
            if amenity.id == amenity_id:
                linked = amenity
                break
    else:
        for amenity in place_obj.amenity_ids:
            if amenity == amenity_id:
                linked = amenity_obj
                break

    if getenv("HBNB_TYPE_STORAGE") == "db":
        if linked is not None:
            return jsonify(linked), 200
        else:
            place_obj.amenities.append(amenity_obj)
            place_obj.save()
            res = jsonify(amenity_obj)
            res.status_code = 201
            return res
    else:
        if linked is not None:
            return jsonify(linked)
        else:
            place_obj.amenity_ids.append(amenity_id)
            place_obj.save()
            res = jsonify(amenity_obj)
            res.status_code = 201
            return res
