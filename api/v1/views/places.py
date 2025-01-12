#!/usr/bin/python3
"""index """

from models import storage, storage_t
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User


@app_views.route("cities/<city_id>/places", methods=['GET', 'POST'])
def places_without_id(city_id):
    """Create a new place or return all the places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places_list = [place.to_dict() for place in city.places]
        return jsonify(places_list)

    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, "Not a JSON")
        user_id = json.get('user_id')
        if user_id is None:
            abort(400, "Missing user_id")
        if json.get('name') is None:
            abort(400, "Missing name")
        if storage.get(User, user_id) is None:
            abort(404)
        json['city_id'] = city_id
        place = Place(**json)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['GET', 'PUT', 'DELETE'])
def places_with_id(place_id=None):
    """Perform READ UPDATE DELETE operations on a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place.delete()
        del place
        return jsonify({})

    if request.method == 'PUT':
        json = request.get_json()
        if json is None:
            abort(400, "Not a JSON")
        place.update(**json)
        return jsonify(place.to_dict())


@app_views.route("/places_search", methods=['POST'])
def search_places():
    """Search for places based on the request body"""
    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")

    places = [p for p in storage.all(Place).values()]
    states_ids = json.get('states', None)
    cities_ids = json.get('cities', None)
    amenities_ids = json.get('amenities', None)

    if states_ids and len(states_ids) > 0:
        cities = storage.all(City)
        state_cities = set([city.id for city in cities.values()
                            if city.state_id in states_ids])
    else:
        state_cities = set()

    if cities_ids and len(cities_ids) > 0:
        cities_ids = set([c_id for c_id in cities_ids
                          if storage.get(City, c_id)])
        state_cities = state_cities.union(cities_ids)

    if len(state_cities) > 0:
        places = [p for p in places if p.city_id in state_cities]

    result = []
    if amenities_ids and len(amenities_ids) > 0:
        amenities_ids = set([a_id for a_id in amenities_ids
                             if storage.get(Amenity, a_id)])

        for place in places:
            a_ids = None
            if storage_t == "db" and place.amenities:
                a_ids = [a.id for a in place.amenities]
                del place.amenities
            elif len(place.amenities) > 0:
                a_ids = p.amenity_ids
            if a_ids and all([a_id in a_ids for a_id in amenities_ids]):
                result.append(place.to_dict())
    else:
        result = [p.to_dict() for p in places]

    return jsonify(result)
