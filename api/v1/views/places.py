#!/usr/bin/python3
"""places.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getPlaces(city_id):
    ''' get place information for all places in a specified city '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    placesList = []
    for place in city.places:
        placesList.append(place.to_dict())
    return jsonify(placesList)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def getPlace(place_id):
    ''' get place information for specified place_id '''
    placeSelect = storage.get("Place", place_id)
    if placeSelect is None:
        abort(404)
    return jsonify(placeSelect.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id):
    ''' deletes a place based on its place_id '''
    placeDelete = storage.get("Place", place_id)
    if placeDelete is None:
        abort(404)
    placeDelete.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def postPlace(city_id):
    ''' create a new place '''
    city = storage.get("City", city_id)
    user = storage.get("User", kwargs['user_id'])
    kwargs = request.get_json()
    kwargs['city_id'] = city_id
    place = Place(**kwargs)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in kwargs:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if user is None:
        abort(404)
    if 'name' not in kwargs:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def putPlace(place_id):
    """update a place"""
    placeUpdate = storage.get("Place", place_id)
    if placeUpdate is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, value in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(place, attr, value)
    placeUpdate.save()
    return jsonify(placeUpdate.to_dict())
