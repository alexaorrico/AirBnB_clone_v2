#!/usr/bin/python3
"""Flask route for place model"""

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.place import Place
from models.city import City
from models.amenity import Amenity
from os import environ
STOR_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places(city_id=None):
    """route to return all cities"""

    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404, 'Not found')

    if request.method == "GET":
        places_dict = storage.all(Place)
        places_list = [obj.to_dict()
                       for obj in places_dict.values()
                       if obj.city_id == city_id
                       ]
        return jsonify(places_list)

    if request.method == "POST":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        if request_json.get("user_id") is None:
            abort(400, "Missing user_id")
        if storage.get("User", request_json.get("user_id")) is None:
            abort(404, "Not found")
        if request_json.get("name") is None:
            abort(400, "Missing name")

        request_json["city_id"] = city_id
        newPlace = Place(**request_json)
        newPlace.save()
        return make_response(jsonify(newPlace.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"])
def place(place_id=None):
    """Get, update or delete place with place id"""
    place_obj = storage.get(Place, place_id)

    if place_obj is None:
        abort(404, "Not found")

    if request.method == "GET":
        return jsonify(place_obj.to_dict())

    if request.method == "DELETE":
        place_obj.delete()
        storage.save()
        return jsonify({})

    if request.method == "PUT":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        place_obj.update(request_json)
        return make_response(jsonify(place_obj.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """Searching places in cities with places_search endpoint"""
    all_places = [place for place in storage.all(Place).values()]
    request_json = request.get_json()
    if request_json is None:
        abort(400, 'Not a JSON')

    states = request_json.get('states')
    if states and len(states) > 0:
        all_cities = storage.all(City)
        state_cities = set([city.id for city in all_cities.values()
                            if city.state_id in states])
    else:
        state_cities = set()
    cities = request_json.get('cities')
    if cities and len(cities) > 0:
        cities = set([
            city_id for city_id in cities if storage.get(City, city_id)])
        state_cities = state_cities.union(cities)
    amenities = request_json.get('amenities')
    if len(state_cities) > 0:
        all_places = [p for p in all_places if p.city_id in state_cities]
    elif amenities is None or len(amenities) == 0:
        output = [place.to_dict() for place in all_places]
        return jsonify(output)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set([
            a_id for a_id in amenities if storage.get(Amenity, a_id)])
        for p in all_places:
            p_amenities = None
            if STOR_TYPE == 'db' and p.amenities:
                p_amenities = [a.id for a in p.amenities]
            elif len(p.amenities) > 0:
                p_amenities = p.amenities
            if p_amenities and all([a in p_amenities for a in amenities]):
                places_amenities.append(p)
    else:
        places_amenities = all_places
    output = [place.to_dict() for place in places_amenities]
    return jsonify(output)
