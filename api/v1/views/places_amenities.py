#!/usr/bin/python3
"""blueprint for the places"""

from api.v1.views import app_views, storage_type
from flask import jsonify, abort, request, make_response
from markupsafe import escape
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.get('/places/<place_id>/amenities', strict_slashes=False)
def get_amenities_of_place(place_id):
    """this is the view for the /api/v1/places/[SLUG]/amenities
        endpoint"""
    res = storage.get(Place, escape(place_id))
    if not res:
        abort(404)
    if storage_type == "db":
        res = [x.to_dict() for x in res.amenities]
    else:
        res_tmp = res.amenity_ids
        res = [storage.get(Amenity, x).to_dict() for x in res_tmp]
    return jsonify(res)


@app_views.delete('/places/<place_id>/amenities/<amenity_id>',
                  strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """this is the view for the /api/v1/places/[SLUG]/amenities/[SLUG]
        endpoint"""
    res = storage.get(Place, escape(place_id))
    res_amenity = None
    if not res:
        abort(404)
    if storage_type == "db":
        res = [x for x in res.amenities if x.id == amenity_id]
        if len(res) < 1:
            abort(404)
        res_amenity = res[0]
    else:
        res_tmp = res.amenity_ids
        res = [storage.get(Amenity, x) for x in res_tmp
               if x == amenity_id]
        if len(res) < 1:
            abort(404)
        res_amenity = res[0]
    storage.delete(res_amenity)
    storage.save()
    return jsonify({})


@app_views.post("/places/<place_id>/amenities/<amenity_id>")
def create_place_amenity(place_id, amenity_id):
    """this is the view for the /api/v1/places/[SLUG]/amenities/[SLUG]
        endpoint"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if storage_type == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
