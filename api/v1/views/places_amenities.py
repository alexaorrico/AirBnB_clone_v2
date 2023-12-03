#!/usr/bin/python3
""" Handles Place Amenities"""

from os import environ
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from flask import abort, jsonify, make_response


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_p_amenity(place_id):
    """
    Gets all the places amenities
    """
    get_p = storage.get(Place, place_id)

    if not get_p:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        instance = [item.to_dict() for item in get_p.amenities]
    else:
        instance = [storage.get(Amenity, id).to_dict()
                    for id in get_p.amenity_ids]
    return jsonify(instance)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_p_a(place_id, amenity_id):
    """
    Delestes the place amenity
    """
    get_p = storage.get(Place, place_id)
    if not get_p:
        abort(404)
    get_a = storage.get(Amenity, amenity_id)
    if not get_a:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if get_a not in get_p.amenities:
            abort(404)
        get_p.amenities.remove(get_a)
    else:
        if amenity_id not in get_p.amenity_ids:
            abort(404)
        get_p.amenity_ids.remove(amenity_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_p_a(place_id, amenity_id):
    """
    Create a place amenity
    """
    get_p = storage.get(Place, place_id)
    if not get_p:
        abort(404)
    get_a = storage.get(Amenity, amenity_id)

    if not get_a:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if get_a in get_p.amenities:
            a_file = jsonify(get_a.to_dict())
            return make_response(a_file, 200)
        else:
            get_p.amenities.append(get_a)
    else:
        if amenity_id in get_p.amenity_ids:
            file = jsonify(get_a.to_dict())
            return make_response(file, 200)
        else:
            get_p.amenity_ids.append(amenity_id)
    storage.save()
    json_file = jsonify(get_a.to_dict())
    return make_response(json_file, 201)
