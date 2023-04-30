#!/usr/bin/python3
"""
Places-Amenities file
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_places_amenities(place_id):
    """ Function that returns a JSON """
    the_obj = storage.get(Place, place_id)
    if the_obj is None:
        abort(404)
    my_list = []
    if (storage_t == 'db'):
        for obj in the_obj.amenities:
            my_list.append(obj.to_dict())
    else:
        for obj in the_obj.amenities:
            my_list.append(obj.to_dict())
    return jsonify(my_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place_amenity(place_id, amenity_id):
    the_obj = storage.get(Place, place_id)
    if the_obj is None:
        abort(404)
    the_obj_amenity = storage.get(Amenity, amenity_id)
    if the_obj_amenity is None:
        abort(404)
    if storage_t == 'db':
        if the_obj_amenity not in the_obj.amenities:
            abort(404)
        the_obj.amenities.remove(the_obj_amenity)
    else:
        if the_obj_amenity.id not in the_obj.amenity_ids:
            abort(404)
        the_obj.amenity_ids.remove(the_obj_amenity.id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    the_obj = storage.get(Place, place_id)
    if the_obj is None:
        abort(404)
    the_amenity = storage.get(Amenity, amenity_id)
    if the_amenity is None:
        abort(404)
    if storage_t == 'db':
        if the_amenity in the_obj.amenities:
            return make_response(jsonify(the_amenity.to_dict()), 200)
        the_obj.amenities.append(the_amenity)
    else:
        if the_amenity not in the_obj.amenity_ids:
            return make_response(jsonify(the_amenity.to_dict()), 200)
        the_obj.amenity_ids.append(the_amenity.id)
    storage.save()
    return make_response(jsonify(the_amenity.to_dict()), 201)
