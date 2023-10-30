#!/usr/bin/python3
"""handles all default RESTFul API actions for places and amenity objects"""
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
def place_amenities_objs(place_id):
    '''Retrieves the list of all Amenity objects of a Place'''
    place = storage.get(Place, str(place_id))
    if place is None:
        abort(404)
    place_amenities = [amenity.to_dict() for amenity in place.amenities]
    res = jsonify(place_amenities)
    res.status_code = 200
    return res


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_place_amenity(place_id, amenity_id):
    '''Deletes a Amenity object to a Place'''
    linked = False
    place_obj = storage.get(Place, str(place_id))
    amenity_obj = storage.get(Amenity, str(amenity_id))
    if place_obj is None or amenity_obj is None:
        abort(404)
    for amenity in place_obj.amenities:
        if amenity.id == str(amenity_id):
            if getenv("HBNB_TYPE_STORAGE") == "db":
                place_obj.amenities.remove(amenity)
            else:
                place_obj.amenity_ids.remove(amenity.id)
            linked = True
            place_obj.save()
            break
    if linked is False:
        abort(404)
    else:
        res = jsonify({})
        res.status_code = 200
        return res


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def link_amenity_to_place(place_id, amenity_id):
    '''Link a Amenity object to a Place'''
    place_obj = storage.get(Place, str(place_id))
    amenity_obj = storage.get(Amenity, str(amenity_id))
    if place_obj is None or amenity_obj is None:
        abort(404)

    for amenity in place_obj.amenities:
        if amenity.id == str(amenity_id):
            return jsonify(amenity.to_dict())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_obj.amenities.append(amenity_obj)
    else:
        place_obj.amenities = amenity_obj
    place_obj.save()
    res = jsonify(amenity_obj.to_dict())
    res.status_code = 201
    return res
