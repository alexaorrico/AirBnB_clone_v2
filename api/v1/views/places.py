#!/usr/bin/python3
"""
Router for handling API calls on Place objects
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def allPlaceOfCity(city_id):
    """Retrieve all places object of a city"""
    places = []
    try:
        city = storage.get(City, city_id)
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places), 200
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def onePlace(place_id):
    """Retrieve one Place"""
    try:
        place = storage.get(Place, place_id).to_dict()
        return jsonify(place), 200
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id):
    """Delete one Place"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def createPlace(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        return jsonify(error='Not a JSON'), 400

    body = request.get_json()
    if 'user_id' not in body:
        return jsonify(error='Missing user_id'), 400

    user = storage.get(User, body.get('user_id'))
    if not user:
        abort(404)

    if 'name' not in body:
        return jsonify(error='Missing name'), 400

    newPlace = Place(name=body.get('name'), city_id=city_id,
                     user_id=body.get('user_id'))
    newPlace.save()
    return jsonify(newPlace.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updatePlace(place_id):
    """Updates a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        if not request.is_json:
            return jsonify(error='Not a JSON'), 400

        forbidden_keys = ['id', 'state_id', 'created_at', 'updated_at']

        body = request.get_json()
        for k, v in body.items():
            if k not in forbidden_keys:
                setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict()), 200
