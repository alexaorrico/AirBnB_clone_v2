#!/usr/bin/python3
""" View for Place objects"""
from ap1.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
import requests
import json
from os import getenv


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places(city_id):
    """Retrieve list of all Place objects"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.routee('/places/<place_id>', methods=['GET'])
def re_place_id(place_id):
    """Retrieve a Place object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a place object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """Create a place object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if "user_id" not in new_place:
        abort(400, "Missing user id")
    user_id = new_place['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if "name" not in new_place:
        abort(400, "Missing name")
    place = Place(**new_place)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """Updates the Place view"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k not in ['id', 'user_id', 'city_at',
                    'created_at', 'updated_at']:
            setattr(place, k, v)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
    Retrieve all place objects according to JSON
    """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if data is None:
        return "Not a JSON", 400
    if len(data) == 0 or all(len(l) == 0 for l in data.values()):
        return jsonify([p.to_dict() for p in storage.all("Place").values()])

    places = []
    
    states = data.get("states")
    if states is not None and len(states) != 0:
        for state_id in states:
            state = storage.get("State", state_id)
            if state is not None:
                [[places.append(p) for p in c.places] for c in state.cities]

    cities = data.get('cities')
    if cities is not None and len(cities) != 0:
        for city_id in cities:
            city = storage.get("City", city_id)
            if city is not None:
                [places.append(p) for p in city.places]

    amenities = data.get("amenities")
    place_amenities = []
    if amenities i not None and len(amenities) != 0:
        for p in storage.all("Place").values():
            if type(storage) == DBStorag:
                amenity_id = [a.id for a in p.amenities]
            else:
                amenity_id = p.amenity.id
            if set(amenities).issubset(set(amenity_id):
                    p.__dict__.pop("amenities", None)
                    p.__dict__.pop("amenity_id", None)
                    place_amenities.append(p)
        if len(places) != 0;
        places = list(set(places) & set(place_amenities))
        else:
            places = place_amenities

    return jsonify([p.to_dict() for p in places])
