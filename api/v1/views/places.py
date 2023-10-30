#!/usr/bin/python3
"""Module containing a Flask Blueprint routes that handles
all default RESTFul API actions for Place resource"""
from api.v1.views import app_views
from flask import abort, make_response, jsonify, request
from markupsafe import escape
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from os import getenv


def retrive_object(cls, id):
    """Retrives a resource based on given class and id."""
    obj = storage.get(cls, escape(id))
    if obj is None:
        abort(404)
    return (obj)


def validate_request_json(request):
    """Checks validity of request's json content"""
    if not request.is_json:
        abort(make_response(jsonify(error="Not a JSON"), 400))
    req_json = request.get_json()
    if request.method == 'POST':
        if 'user_id' not in req_json:
            abort(make_response(jsonify(error="Missing user_id"), 400))
        retrive_object(User, req_json['user_id'])
        if 'name' not in req_json:
            abort(make_response(jsonify(error="Missing name"), 400))
    return (req_json)


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def cities_places_get(city_id):
    """Returns a list of places for a City resource with given id"""
    obj = retrive_object(City, city_id)
    # Error when HBNB_TYPE_STORAGE is not db cause no City.places getter.
    # To fix it, added a conditonal below. (OR ADD GETTER City.places)
    if getenv('HBNB_TYPE_STORAGE') == 'db':  # use getter
        places = [place.to_dict() for place in obj.places]
    else:  # get places and generate list based on place.city_id
        all_places = storage.all(Place).values()
        places = [place.to_dict() for place in all_places
                  if place.city_id == obj.id]
    return (jsonify(places))


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def places_get(place_id):
    """Returns a Place resource based on given id"""
    obj = retrive_object(Place, place_id)
    return (jsonify(obj.to_dict()))


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def places_delete(place_id):
    """Deletes a Place resource based on given id"""
    obj = retrive_object(Place, place_id)
    storage.delete(obj)
    storage.save()
    return (jsonify({}))


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def cities_places_post(city_id):
    """Creates a Place resource in a City of given id
    if request content is valid."""
    obj = retrive_object(City, city_id)
    req_json = validate_request_json(request)
    req_json['city_id'] = obj.id
    new_place = Place(**req_json)
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def places_put(place_id):
    """Updates a Place resource of given id if request content is valid."""
    obj = retrive_object(Place, place_id)
    req_json = validate_request_json(request)
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore:
            setattr(obj, key, value)
    obj.save()
    return (jsonify(obj.to_dict()))
