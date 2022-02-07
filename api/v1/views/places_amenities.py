#!/usr/bin/python3
'''places amenities relationship blueprint'''

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, storage_t
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def getAmenitiesInPlace(place_id=None):
    '''get all amenities in a place'''
    if place_id is None:
        abort(404)
    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)

    res = []
    if storage_t != 'db':
        amens = storage.all(Amenity)
        for amen in amens.values():
            if amen.id in pl.amenity_ids:
                res.append(amen)
    else:
        res = pl.amenities

    return jsonify([amen.to_dict() for amen in res])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenityFromPlace(place_id=None, amenity_id=None):
    '''deletes an amenity from a place'''
    if place_id is None or amenity_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if storage_t != 'db':
        if amenity.id not in place.amenity_ids:
            abort(404)
        index = None
        for idx, id in enumerate(place.amenity_ids):
            if amenity.id == id:
                index = idx
                break
        del place.amenity_ids[index]
        place.save()
    else:
        index = None
        for idx, amen in enumerate(place.amenities):
            if amen.id == amenity.id:
                index = idx
                break
        if index is None:
            abort(404)
        del place.amenities[index]
        place.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def linkAmenityToPlace(place_id=None, amenity_id=None):
    '''link an amenity to a place'''
    if place_id is None or amenity_id is None:
        abort(404)

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if storage_t != 'db':
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)
            place.save()
            return make_response(jsonify(amenity.to_dict()), 201)
    else:
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
            place.save()
            return make_response(jsonify(amenity.to_dict()), 201)
