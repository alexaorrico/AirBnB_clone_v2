#!/usr/bin/python3
"""Create a new view for State objects that handles all default RestFul API"""


from flask import jsonify, abort, request
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def getPlace(place_id=None):
    """Get places for id endpoint"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_cities(city_id=None):
    """view for City objects"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    else:
        placesL = city.places
        placesList = []
        for place in placesL.values():
            placesList.append(place.to_dict())
        return jsonify(placesList)


@app_views.route('places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id=None):
    """Deletes a Place object"""
    id_place = storage.get('Place', place_id)
    if place_id is None:
        abort(404)
    else:
        storage.delete(id_place)
        storage.save()
        return jsonify({}), 200


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def places_create(city_id=None):
    """Creates new states"""
    res = request.get_json()
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if res is None:
        abort(400, "Not a JSON")
    if 'name' not in res:
        abort(400, "Missing name")
    if 'user_id' not in res:
        abort(400, "Missing user_id")
    user = storage.get('User', res['user_id'])
    if user is None:
        abort(404)

    res['city_id'] = city_id
    newobj = Place(**res)
    storage.new(newobj)
    storage.save()
    return jsonify(newobj.to_dict()), 201


@app_views.route('places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def places_put(place_id=None):
    """updates a value from an instance"""
    place = storage.get('Place', place_id)
    res = request.get_json()

    if place_id is None:
        abort(404)
    if res is None:
        abort(400, "Not a JSON")

    for k, v in res.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
