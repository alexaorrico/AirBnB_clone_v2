#!/usr/bin/python3
""" Place Amenities"""

from os import environ
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from flask import abort, jsonify, make_response


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenity(place_id):
    """
    Gets places amenities
    """
    get_pl = storage.get(Place, place_id)

    if not get_pl:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        instance = [item.to_dict() for item in get_pl.amenities]
    else:
        instance = [storage.get(Amenity, id).to_dict()
                    for id in get_pl.amenity_ids]
    return jsonify(instance)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_a(place_id, amenity_id):
    """
    Delestes place amenity of given id
    """
    get_pl = storage.get(Place, place_id)
    if not get_pl:
        abort(404)
    get_am = storage.get(Amenity, amenity_id)
    if not get_am:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if get_am not in get_pl.amenities:
            abort(404)
        get_pl.amenities.remove(get_am)
    else:
        if amenity_id not in get_pl.amenity_ids:
            abort(404)
        get_pl.amenity_ids.remove(amenity_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_place_a(place_id, amenity_id):
    """
    Creates place amenity
    """
    get_pl = storage.get(Place, place_id)
    if not get_pl:
        abort(404)
    get_am = storage.get(Amenity, amenity_id)

    if not get_am:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if get_am in get_pl.amenities:
            a_file = jsonify(get_am.to_dict())
            return make_response(a_file, 200)
        else:
            get_pl.amenities.append(get_am)
    else:
        if amenity_id in get_pl.amenity_ids:
            file = jsonify(get_am.to_dict())
            return make_response(file, 200)
        else:
            get_pl.amenity_ids.append(amenity_id)
    storage.save()
    json_file = jsonify(get_am.to_dict())
    return make_response(json_file, 201)
