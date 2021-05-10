#!/usr/bin/python3
"""
    This is the places page handler for Flask.
"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request

from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<id>/places', methods=['GET', 'POST'])
def cities_id_places(id):
    """
        Flask route at /cities/<id>/places.
    """
    city = storage.get(City, id)
    if (city):
        if request.method == 'POST':
            kwargs = request.get_json()
            if not kwargs:
                return {"error": "Not a JSON"}, 400
            if "user_id" not in kwargs:
                return {"error": "Missing user_id"}, 400

            user = storage.get(User, kwargs.get("user_id", None))
            if (user):
                if "name" not in kwargs:
                    return {"error": "Missing name"}, 400
                new_place = Place(city_id=id, **kwargs)
                new_place.save()
                return new_place.to_dict(), 201

        elif request.method == 'GET':
            return jsonify([p.to_dict() for p in city.places])
    abort(404)


@app_views.route('/places/<id>', methods=['GET', 'DELETE', 'PUT'])
def places_id(id):
    """
        Flask route at /places/<id>.
    """
    place = storage.get(Place, id)
    if (place):
        if request.method == 'DELETE':
            place.delete()
            storage.save()
            return {}, 200

        elif request.method == 'PUT':
            kwargs = request.get_json()
            if not kwargs:
                return {"error": "Not a JSON"}, 400
            for k, v in kwargs.items():
                if k not in ["id", "user_id", "city_id",
                             "created_at", "updated_at"]:
                    setattr(place, k, v)
            place.save()
        return place.to_dict()
    abort(404)


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
        Flask route at /places_search
    """
    kwargs = request.get_json()
    if not kwargs:
        return {"error": "Not a JSON"}, 400
    states = kwargs.get('states', [])
    cities = kwargs.get('cities', [])
    amenities = kwargs.get('amenities', [])
    if states == cities == []:
        places = storage.all("Place").values()
    else:
        places = []
        for state_id in states:
            state = storage.get(State, state_id)
            for city in state.cities:
                state_cities = state.cities
                if city.id not in cities:
                    cities.append(city.id)
        for city_id in cities:
            city = storage.get(City, city_id)
            for place in city.places:
                places.append(place)
    search_result = []
    amenity_objs = []
    for amenity_id in amenities:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            amenity_objs.append(amenity)
    for place in places:
        amenities_cnt = 0
        for amenity in amenity_objs:
            if amenity not in place.amenities:
                amenities_cnt += 1
        if amenities_cnt == 0:
            search_result.append(place.to_dict())

    return jsonify(search_result)
