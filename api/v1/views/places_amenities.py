#!/usr/bin/python3
"""
    HBNB_V3: Task 14
"""
from api.v1.views.index import app_views, Place, Amenity
from models import storage
from flask import jsonify, request, abort, make_response
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def viewalltheamenitythingsinsideaplacething(place_id):
    """Retrieves the list of all State objects"""
    if storage.get(Place, place_id) is None:
        abort(404)
    if request.method == 'GET':
        plc = storage.get(Place, place_id)
        if getenv("HBNB_TYPE_STORAGE") == "db":
            atl = plc.amenities
        else:
            atl = plc.amenity_ids
        amnt = [amnty.to_dict() for amnty in atl]
        return jsonify(amnt)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'POST'])
def amenityinplaceidtimechea(place_id, amenity_id):
    """Handles a state object with said id depending on HTTP request"""
    ptl = storage.get(Place, place_id)
    atl = storage.get(Amenity, amenity_id)
    if ptl is not None and atl is not None:
        if request.method == 'DELETE':
            if getenv("HBNB_TYPE_STORAGE") == "db":
                if atl in ptl.amenities:
                    ptl.amenities.remove(atl)
                    ptl.save()
                else:
                    abort(404)
            else:
                if atl.__dict__.get("id") in ptl.amenity_ids:
                    ptl.amenities.remove(atl.__dict__.get("id"))
                    ptl.save()
                else:
                    abort(404)
            return jsonify({})
        if request.method == 'POST':
            if getenv("HBNB_TYPE_STORAGE") == "db":
                if atl in ptl.amenities:
                    return jsonify(atl.to_dict()), 200
                else:
                    ptl.amenities.append(atl)
                    ptl.save()
                    return jsonify(atl.to_dict()), 201
            else:
                if atl.__dict__.get("id") in ptl.amenity_ids:
                    return jsonify(atl.to_dict()), 200
                else:
                    ptl.amenities.append(atl.__dict__.get('id'))
                    ptl.save()
                    return jsonify(atl.to_dict()), 201
    else:
        abort(404)
