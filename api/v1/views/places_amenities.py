#!/usr/bin/python3
"""
module for CRUD LINK between Place <--> Amenity
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities_of_place(place_id):
    """ retrieve the list amenities belongs to place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    json_obj = [am.to_dict() for am in place.amenities]
    return jsonify(json_obj)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity_for_place(place_id, amenity_id):
    """ remove amanity belongs to place from stoarge"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    am_of_place = place.amenities
    obj_amenity = None
    for am in am_of_place:
        if am.id == amenity_id:
            obj_amenity = am
            break
    if not obj_amenity:
        abort(404)
    am_of_place.remove(obj_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_amenity_to_place(place_id, amenity_id):
    """ create new link amenity place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    am_of_place = place.amenities
    obj_amenity = None
    for am in am_of_place:
        if am.id == amenity_id:
            obj_amenity = am
            break
    if obj_amenity:
        return jsonify(obj_amenity.to_dict()), 200
    else:
        am_of_place.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
