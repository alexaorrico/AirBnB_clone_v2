#!/usr/bin/python3
""" flask module to manage the stored places """
from models.city import City
from models.place import Place
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage


@app_views.route(
    '/cities/<string:city_id>/places',
    strict_slashes=False,
    methods=['GET']
)
def all_places(city_id):
    """ it retrieve all the places """
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    places_list = []
    for place in cities.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route(
    '/places/<string:place_id>',
    strict_slashes=False,
    methods=['GET']
)
def get_place(place_id):
    """ it get the place corresponding to the place_id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    '/places/<string:place_id>',
    strict_slashes=False,
    methods=['DELETE']
)
def delete_place(place_id):
    """ it delete the place corresponding to the place_id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/cities/<string:city_id>/places',
    strict_slashes=False,
    methods=['POST']
)
def create_place(city_id):
    """ it create an place from a http request
    the new place information is expected to be
    json string
    """
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    place_json = request.get_json()
    if place_json is None:
        abort(400, 'Not a JSON')
    if place_json.get('user_id') is None:
        abort(400, "Missing user_id")
    if place_json.get('name') is None:
        abort(400, "Missing name")
    place = Place(**place_json)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route(
    '/places/<string:place_id>',
    strict_slashes=False, methods=['PUT']
)
def update_place(place_id):
    """ it update an place """
    ignored_keys = ['id', 'user_id', 'created_at', 'city_id']
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_json = request.get_json()
    if place_json is None:
        abort(400, 'Not a JSON')

    for key in place_json.keys():
        if key in ignored_keys:
            continue
        if getattr(place, key):
            setattr(place, key, place_json[key])
    storage.save()
    return jsonify(place.to_dict()), 200
