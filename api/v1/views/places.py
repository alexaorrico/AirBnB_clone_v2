#!/usr/bin/python3
""" view for Place objects that handles all default RESTFul API actions """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False,
)
def getPlace(city_id):
    """ Retrieves all Place objects of a city """
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    places = [place.to_dict() for place in cities.places]
    return jsonify(places)


@app_views.route(
    '/places/<place_id>', methods=['GET'],
    strict_slashes=False
)
def getPlaceById(place_id):
    """ Retrieves a Place object by id """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route(
    '/places/<place_id>', methods=['DELETE'],
    strict_slashes=False
)
def deletePlaceById(place_id):
    """ Delete user object by id """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    place_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def newPlace(city_id):
    """ Returns the new Place """
    if city_id not in storage.get(City, city_id):
        abort(404)
    if not request.get_json():
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return (jsonify({'error': 'Missing user_id'}), 400)
    if 'name' not in request.get_json():
        return (jsonify({'error': 'Missing name'}), 400)
    new = request.get_json()
    obj = Place(**new)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route(
    '/places/<place_id>', methods=['PUT'],
    strict_slashes=False
)
def updatePlaceById(place_id):
    """ Update the User object """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict())
