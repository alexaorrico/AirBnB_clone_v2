#!/usr/bin/python3
''' places_amenities.py'''

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv

storage_type = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenity_list(place_id):
    """ list of an objetc in dict form
    """
    places = storage.all('Place')
    for key, place_obj in places.items():
        if place_obj.id == place_id:
            amenities = place_obj.amenities
            amenity_list = [amenity.to_dict() for amenity in amenities]
            return (jsonify(amenity_list))
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity(place_id, amenity_id):
    """ delete the object
    """
    place_obj = storage.get("Place", place_id)
    amenity_obj = storage.get("Amenity", amenity_id)
    if not place_obj or not amenity_obj:
        abort(404)
    for obj in place_obj.amenities:
        if obj.id == amenity_obj.id:
            if storage_type == 'db':
                place_obj.amenities.remove(amenity_obj)
            else:
                place_obj.amenity_ids.remove(amenity_obj)
            place_obj.save()
            return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def create_amenity(place_id, amenity_id):
    """ create an amenity of a city
    """
    place_obj = storage.get("Place", place_id)
    amenity_obj = storage.get("Amenity", amenity_id)
    if not amenity_obj or not place_obj:
        abort(404)
    for obj in place_obj.amenities:
        if obj.id == amenity_obj.id:
            return jsonify(amenity_obj.to_dict())
    if storage_type == 'db':
        place_obj.amenities.append(amenity_obj)
    else:
        place_obj.amenity_id.append(amenity_obj)
    place_obj.save()
    return jsonify(amenity_obj.to_dict()), 201
