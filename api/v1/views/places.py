#!/usr/bin/python3
"""view for Place objects that handles all default RESTFul API actions"""
from flask import jsonify
from flask import abort
from flask import request
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def place(city_id):
    """Retrieves the list of all Place objects"""
    try:
        cities = storage.get(City, city_id)
        PlaceList = []
        for place in cities.places:
            PlaceList.append(place.to_dict())
        return jsonify(PlaceList)
    except:
        abort(404)


@app_views.route("/places/<string:place_id>", methods=['GET'])
def getPlaces(place_id):
    """Retrieves a Place object"""
    try:
        place = storage.get(Place, place_id).to_dict()
        return jsonify(place)
    except:
        abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'])
def deletePlaces(place_id):
    """Deletes a Place object"""
    try:
        storage.delete(Place, place_id)
        storage.save()
        return {}, 200
    except:
        abort(404)


@app_views.route("/cities/<city_id>/places",
                 methods=['POST'], endpoint='placePost')
def postPlaces(city_id):
    """Creates a Place"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    try:
        city = storage.get(City, city_id)
        user = storage.get(User, data['user_id'])
    except:
        abort(404)
    instance = Place(**data)
    instance.city_id = city_id
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'])
def putPlaces(place_id):
    """Updates a Place object"""
    k = "Place." + str(place_id)
    if k not in storage.all():
        abort(404)
    data = request.get_json()
    if not request.is_json:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(storage.all()[k], key, value)
    storage.all()[k].save()
    return jsonify(storage.get(Place, place_id).to_dict()), 200
