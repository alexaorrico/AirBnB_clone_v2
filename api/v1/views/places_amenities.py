#!/usr/bin/python3
"""View between Place objects and Amenity"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from os import getenv

bd = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def places_amenitiesAll(id):
    """ Retrieves [] of all Places amenities objects of a Place """
    ll = []
    place = storage.all('Place')
    for x in place:
        if place[x].id == id:
            vv = place[x].amenities
            for i in vv:
                ll.append(i.to_dict())
            return (jsonify(ll))
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def places_amenitiesDel(place_id, amenity_id):
    """Delete an amenity object from a place"""
    ss = storage.get("Place", place_id)
    aa = storage.get("Amenity", amenity_id)
    if not aa or not ss:
        abort(404)
    for x in ss.amenities:
        if x.id == aa.id:
            if bd == 'db':
                ss.amenities.remove(aa)
            else:
                ss.amenity_ids.remove(aa)
            ss.save()
            return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def places_amenitiesPost(place_id, amenity_id):
    """POST new amenity in id place """
    ss = storage.get("Place", place_id)
    aa = storage.get("Amenity", amenity_id)
    print(aa)
    print("+++++++++++")
    print(ss)
    if not aa or not ss:
        abort(404)
    for x in ss.amenities:
        if x.id == aa.id:
            return jsonify(aa.to_dict())
    if db == 'db':
        ss.amenities.append(aa)
    else:
        ss.amenity_id.append(aa)
    ss.save()
    return jsonify(aa.to_dict()), 201
