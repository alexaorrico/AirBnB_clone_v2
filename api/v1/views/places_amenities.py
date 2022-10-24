#!/usr/bin/python3
"""view for the link between Place objects and Amenity objects that
handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv

storage_type = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities')
def amenties_of_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amn_dict = [amn.to_dict() for amn in place.amenities]
    return(jsonify(amn_dict))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_linked_amenity(place_id, amenity_id):
    """Deletes a Amenity object linked to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    amn = [amn for amn in place.amenities if amn.id == amenity_id]
    if storage_type == 'db':
        place.amenities.remove(amn[0])
    else:
        place.amenity_id.remove(amn[0])
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
def link_amn_to_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    for amn in place.amenities:
        if amn.id == amenity_id:
            return (jsonify(amenity.to_dict()), 200)
    if storage_type == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity)
    amenity.save()
    return (jsonify(amenity.to_dict()), 201)
