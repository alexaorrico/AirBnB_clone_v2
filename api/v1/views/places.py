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


@app_views.post('/places_search')
def places_search_advance():
    """this is the view for the /api/v1/places_search
        endpoint"""
    if not request.get_json():
        return make_response(jsonify("Not a JSON"), 400)
    data = request.get_json()
    states, cities, amenities = None, None, None
    if data and len(data):
        states, cities = data.get('states', None), data.get('cities', None)
        amenities = data.get('amenities', None)
    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        places_list = []
        places_list = [place.to_dict() for place in places]
        return make_response(jsonify(places_list), 200)
    places_list = []
    if states:
        statesObj = [storage.get(State, obj_id) for obj_id in states]
        statesObj = [x for x in statesObj if x]
        for state in statesObj:
            state_cities = [x for x in state.cities if x]
            for city in state_cities:
                places_list.extend(place for place in city.places)
    if cities:
        city_obj = [storage.get(City, obj_id) for obj_id in cities]
        city_obj = [x for x in city_obj if x]
        for city in city_obj:
            for place in city.places:
                if place not in places_list:
                    places_list.append(place)
    if amenities:
        if not places_list:
            places_list = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, obj_id) for obj_id in amenities]
        places_list = [place for place in places_list
                       if all([am in place.amenities
                               for am in amenities_obj])]
    places = []
    for aPlace in places_list:
        filtered = aPlace.to_dict()
        filtered.pop('amenities', None)
        places.append(filtered)
    res = jsonify(places)
    return make_response(res, 200)
