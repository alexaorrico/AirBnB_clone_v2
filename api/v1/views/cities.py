#!/usr/bin/python3
"""blueprint for the cities"""

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


@app_views.get('/states/<state_id>/cities', strict_slashes=False)
def get_cities_of_state(state_id):
    """this is the view for the /api/v1/states/[SLUG]/cities
        endpoint"""
    res = storage.get(State, escape(state_id))
    if not res:
        abort(404)
    res = storage.all(City).values()
    res = [x.to_dict() for x in res if x.state_id == state_id]
    return jsonify(res)


@app_views.get('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """this is the view for the /api/v1/cities/[SLUG]
        endpoint"""
    res = storage.get(City, escape(city_id))
    if not res:
        abort(404)
    res = res.to_dict()
    return jsonify(res)


@app_views.get('/cities', strict_slashes=False)
def get_cities():
    """this is the view for the /api/v1/cities
        endpoint"""
    res = [x.to_dict() for x in storage.all(City).values()]
    print(f"res is {res}")
    return jsonify(res)


@app_views.delete('/cities/<city_id>', strict_slashes=False)
def delete_city(city_id):
    """this is the view for the /api/v1/cities/[SLUG]
        endpoint"""
    res = storage.get(City, escape(city_id))
    if not res:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({})


@app_views.post('/states/<state_id>/cities', strict_slashes=False)
def post_cities_of_state(state_id):
    """this is the view for the /api/v1/states
        endpoint"""
    res = storage.get(State, escape(state_id))
    if not res:
        abort(404)
    try:
        body = request.get_json()
        if 'name' not in body.keys():
            return make_response(jsonify("Missing name"), 400)
        new_city = City(**body)
        new_city.state_id = state_id
        storage.new(new_city)
        storage.save()
        return make_response(jsonify(new_city.to_dict()), 201)
    except Exception as e:
        print(f"exception is : {e}")
        return make_response(jsonify("Not a JSON"), 400)


@app_views.put('/cities/<city_id>', strict_slashes=False)
def put_city(city_id):
    """this is the view for the /api/v1/cities/[SLUG]
        endpoint"""
    res = storage.get(City, escape(city_id))
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
