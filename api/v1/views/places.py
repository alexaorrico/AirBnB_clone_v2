#!/usr/bin/python3
''' cities.py'''

import json
from flask import jsonify, abort, request
import requests
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from os import getenv


@app_views.route("/cities/<city_id>/places",
                 methods=["GET", "POST"],
                 strict_slashes=False)
def get_places(city_id):
    '''Retrieves the list of all Place objects of a City'''
    city_object = storage.get(City, city_id)
    if not city_object:
        abort(404)

    if request.method == "GET":
        places = [place.to_dict() for place in city_object.places]
        return jsonify(places)

    elif request.method == "POST":
        if not request.is_json:
            abort(400, description="Not a JSON")

        if "name" not in request.json:
            abort(400, description="Missing name")

        if "user_id" not in request.json:
            abort(400, description="Missing user_id")

        place_json = request.get_json()

        user = storage.get(User, place_json["user_id"])
        if not user:
            abort(404)

        place_obj = Place(user_id=place_json["user_id"],
                          city_id=city_id,
                          **place_json)
        storage.new(place_obj)
        storage.save()

        return jsonify(place_obj.to_dict()), 201


@app_views.route("/places/<place_id>",
                 methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_place_id(place_id):
    '''Retrieves a Place object'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == "GET":
        return jsonify(place.to_dict())

    elif request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        if not request.is_json:
            abort(400, description="Not a JSON")

        place_json = request.get_json()
        not_needed = ["id", "created_at", "updated_at", "user_id", "city_id"]
        for attr, attr_value in place_json.items():
            if attr not in not_needed:
                setattr(place, attr, attr_value)
        place.save()
        return jsonify(place.to_dict()), 200


@app_views.route("/places_search",
                 methods=["POST"],
                 strict_slashes=False)
def search_place():
    """
    Retrieves all Place objects depending of
    the JSON in the body of the request
    """
    body_r = request.get_json()
    if body_r is None:
        abort(400, "Not a JSON")

    if not body_r or (
            not body_r.get('states') and
            not body_r.get('cities') and
            not body_r.get('amenities')
    ):
        places = storage.all(Place)
        return jsonify([place.to_dict() for place in places.values()])

    places = []

    if body_r.get('states'):
        states = [storage.get("State", id) for id in body_r.get('states')]

        for state in states:
            for city in state.cities:
                for place in city.places:
                    places.append(place)

    if body_r.get('cities'):
        cities = [storage.get("City", id) for id in body_r.get('cities')]

        for city in cities:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if not places:
        places = storage.all(Place)
        places = [place for place in places.values()]

    if body_r.get('amenities'):
        ams = [storage.get("Amenity", id) for id in body_r.get('amenities')]
        i = 0
        limit = len(places)
        HBNB_API_HOST = getenv('HBNB_API_HOST')
        HBNB_API_PORT = getenv('HBNB_API_PORT')

        port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
        first_url = "http://0.0.0.0:{}/api/v1/places/".format(port)
        while i < limit:
            place = places[i]
            url = first_url + '{}/amenities'
            req = url.format(place.id)
            response = requests.get(req)
            am_d = json.loads(response.text)
            amenities = [storage.get("Amenity", o['id']) for o in am_d]
            for amenity in ams:
                if amenity not in amenities:
                    places.pop(i)
                    i -= 1
                    limit -= 1
                    break
            i += 1
    return jsonify([place.to_dict() for place in places])
