#!/usr/bin/python3
"""blueprint for the places"""

from api.v1.views import app_views
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


@app_views.get('/cities/<place_id>/places', strict_slashes=False)
def get_places_of_city(place_id):
    """this is the view for the /api/v1/cities/[SLUG]/places
        endpoint"""
    res = storage.get(City, escape(place_id))
    if not res:
        abort(404)
    res = storage.all(Place).values()
    res = [x.to_dict() for x in res if x.place_id == place_id]
    return jsonify(res)


@app_views.get('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """this is the view for the /api/v1/places/[SLUG]
        endpoint"""
    res = storage.get(Place, escape(place_id))
    if not res:
        abort(404)
    res = res.to_dict()
    return jsonify(res)


@app_views.get('/places', strict_slashes=False)
def get_places():
    """this is the view for the /api/v1/places
        endpoint"""
    res = [x.to_dict() for x in storage.all(Place).values()]
    return jsonify(res)


@app_views.delete('/places/<place_id>', strict_slashes=False)
def delete_place(place_id):
    """this is the view for the /api/v1/places/[SLUG]
        endpoint"""
    res = storage.get(Place, escape(place_id))
    if not res:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({})


@app_views.post('/cities/<city_id>/places', strict_slashes=False)
def post_place_of_cities(city_id):
    """this is the view for the /api/v1/states
        endpoint"""
    res = storage.get(City, escape(city_id))
    if not res:
        abort(404)
    try:
        body = request.get_json()
        if 'name' not in body.keys():
            return make_response(jsonify("Missing name"), 400)
        if 'user_id' not in body.keys():
            return make_response(jsonify("Missing user_id"), 400)
        new_place = Place(**body)
        new_place.city_id = city_id
        storage.new(new_place)
        storage.save()
        return make_response(jsonify(new_place.to_dict()), 201)
    except Exception as e:
        # print(f"exception is : {e}")
        return make_response(jsonify("Not a JSON"), 400)


@app_views.put('/places/<place_id>', strict_slashes=False)
def put_place(place_id):
    """this is the view for the /api/v1/places/[SLUG]
        endpoint"""
    res = storage.get(Place, escape(place_id))
    ignore_keys = ["id", "created_at", "updated_at"]
    if not res:
        abort(404)
    try:
        body = request.get_json()
        for key in body:
            if key not in ignore_keys:
                res.__dict__[key] = body[key]
        res.save()
        storage.save()
        return make_response(jsonify(res.to_dict()), 200)
    except Exception as e:
        return make_response(jsonify("Not a JSON"), 400)
