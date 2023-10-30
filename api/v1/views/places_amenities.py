#!/usr/bin/python3
""" view for place """
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def retrieve_amenities(place_id):
    """ function to retrieve related reviews """
    if place_id is None:
        return abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    amenities = place.amenities
    list_amenity = []
    for amenity in amenities:
        list_amenity.append(amenity.to_dict())
    return jsonify(list_amenity)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def deleteAmenity(place_id, amenity_id):
    """ post a new place """
    if place_id is None or amenity_id is None:
        return abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    amenities = place.amenities
    if storage_t == 'db':
        found = 0
        for ameniti in amenities:
            if ameniti.id == amenity_id:
                found = 1
                break
        if found == 1:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
        else:
            return abort(404)
    else:
        found = 0
        ids = place.amenity_ids
        for id in ids:
            if id == amenity_id:
                ids.remove(id)
                found = 1
                break
            if found == 1:
                return jsonify({}), 200
            else:
                return abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def postAmenity(place_id, amenity_id):
    """ post a new place """
    if place_id is None or amenity_id is None:
        return abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    amenities = place.amenities
    found = 0
    for ameniti in amenities:
        if ameniti.id == amenity_id:
            found = 1
            break
    if found == 1:
        return jsonify(amenity.to_dict()), 200
    else:
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
