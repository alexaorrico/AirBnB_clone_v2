#!/usr/bin/python3
""" API REST for Place Amenities """
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request
from os import getenv


@app_views.route('/places/<place_id>/amenities')
def pl_amenity_all(place_id):
    """ Route return all amenities in place referenced id """
    my_place = storage.get('Place', place_id)
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        return jsonify(list(map(lambda x: x.to_dict(), my_place.amenities)))
    else:
        return jsonify(my_place.amenity_ids)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_pl_amenity_id(place_id, amenity_id):
    """ Route delete amenities with referenced placeid  & amenityid"""
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    my_amenity = storage.get('Amenity', amenity_id)
    if my_amenity is None:
        abort(404)
    if my_amenity not in my_place.amenities:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        my_place.amenities.remove(my_amenity)
    else:
        my_place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def create_pl_amenities(place_id, amenity_id):
    """ Route create link reviews with POST"""
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    my_amenity = storage.get('Amenity', amenity_id)
    if my_amenity is None:
        abort(404)
    if my_amenity in my_place.amenities:
        return jsonify(my_amenity.to_dict()), 200
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        my_place.amenities.append(my_amenity)
        storage.save()        
    else:
        my_place.amenity_ids.append(amenity_id)
    return jsonify(my_amenity.to_dict()), 201
