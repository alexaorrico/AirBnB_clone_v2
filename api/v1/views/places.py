#!/usr/bin/python3
"""
Handles all default RESTful API actions for Place objects
"""

from . import app_views
from models import storage
from models.city import City
from models.place import Place
from flask import abort, jsonify, make_response, request

PLACE_IGNORE_KEYS = {'id', 'user_id', 'city_id', 'created_at', 'updated_at'}


@app_views.route("/cities/<city_id>/places", methods=['GET'])
def get_city_places(city_id):
    """Retrieves the list of all Place objects attached to a City"""
    c = storage.get('City', city_id)
    if c is None:
        abort(404)
    return jsonify([p.to_dict() for p in c.places])


@app_views.route("/places/<place_id>", methods=['GET'])
def get_place(place_id):
    """Retrieves a place given its ID"""
    p = storage.get('Place', place_id)
    if p is None:
        abort(404)
    return jsonify(p.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'])
def del_place(place_id):
    """Deletes a place given its ID"""
    p = storage.get('Place', place_id)
    if p is None:
        abort(404)
    p.delete()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=['POST'])
def post_place(city_id):
    """Creates a place"""
    c = storage.get('City', city_id)
    if c is None:
        abort(404)
    r = request.get_json()
    if r is None:
        abort(make_response(jsonify("Not a JSON"), 400))
    if 'user_id' not in r:
        abort(make_response(jsonify("Missing user_id"), 400))
    u = storage.get('User', r['user_id'])
    if u is None:
        abort(404)
    if 'name' not in r:
        abort(make_response(jsonify("Missing name"), 400))
    r['city_id'] = city_id
    p = Place(**r)
    p.save()
    return make_response(jsonify(p.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'])
def put_place(place_id):
    """Updates a Place at a given ID"""
    p = storage.get('Place', place_id)
    if p is None:
        abort(404)
    r = request.get_json()
    if r is None:
        abort(make_response(jsonify("Not a JSON"), 400))
    for k, v in r.items():
        if k not in PLACE_IGNORE_KEYS:
            setattr(p, k, v)
    p.save()
    return make_response(jsonify(p.to_dict()), 200)


@app_views.route("/places_search", methods=['POST'])
def places_search():
    """Search for a place by state, city, and amenity"""
    params = request.get_json()
    if params is None:
        abort(make_response(jsonify("Not a JSON"), 400))
    amenities = [
        storage.get('Amenity', id) for id in params.get('amenities', [])
    ]
    states_id = set(params.get(
        'states',
        [] if params.get('cities') is not None else [
            s.id for s in storage.all('State').values()]
    ))
    cities_id = set(params.get(
        'cities',
        [] if params.get('states') is not None else [
            c.id for c in storage.all('City').values()
        ]
    ))
    cities_id.update({
        c.id for c in filter(
            lambda c: c.state_id in states_id, storage.all('City').values()
        )
    })
    places = filter(
        lambda p: p.city_id in cities_id and all(map(
            lambda a: a in p.amenities, amenities
        )),
        storage.all('Place').values()
    )
    return jsonify([p.to_dict() for p in places])
