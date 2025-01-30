#!/usr/bin/python3
"""view for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getPlaces(city_id):
    """retrieve list of all Place objects of a City"""
    all_places = storage.all(Place)
    all_cities = storage.all(City)
    places_list = []
    city_ids = [val.id for val in all_cities.values()]
    if city_id not in city_ids:
        return make_response(jsonify({"error": "Not found"}), 404)
    for val in all_places.values():
        if val.city_id == city_id:
            places_list.append(val.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def getPlace(place_id):
    """retrieve a Place object"""
    all_places = storage.all(Place)
    for val in all_places.values():
        if val.id == place_id:
            return jsonify(val.to_dict())
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id):
    """delete a Place object"""
    all_places = storage.all(Place)
    for val in all_places.values():
        if val.id == place_id:
            storage.delete(val)
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def createPlace(city_id):
    """create a Place"""
    all_cities = storage.all(City)
    all_users = storage.all(User)
    places_list = []
    city_ids = [val.id for val in all_cities.values()]
    user_ids = [val.id for val in all_users.values()]
    if city_id not in city_ids:
        return make_response(jsonify({"error": "Not found"}), 404)
    try:
        data = request.get_json()
        if "user_id" not in data:
            return make_response("Missing user_id", 400)
        if data['user_id'] not in user_ids:
            return make_response(jsonify({"error": "Not found"}), 404)
        if "name" not in data:
            return make_response("Missing name", 400)
        data['city_id'] = city_id
        new_place = Place(**data)
        for key, value in data.items():
            setattr(new_place, key, value)
            storage.new(new_place)
            storage.save()
            return make_response(jsonify(new_place.to_dict()), 201)
    except Exception as e:
        print(e)
        return make_response("Not a JSON", 400)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updatePlace(place_id):
    """update a Place object"""
    all_places = storage.all(Place)
    try:
        data = request.get_json()
        for val in all_places.values():
            if val.id == place_id:
                for key, value in data.items():
                    setattr(val, key, value)
                storage.save()
                return make_response(jsonify(val.to_dict()), 200)
        return make_response(jsonify({"error": "Not found"}), 404)
    except Exception as e:
        return make_response("Not a JSON", 400)
