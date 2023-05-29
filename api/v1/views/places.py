#!/usr/bin/python3
"""RESTful API action for City object"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models import storage
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=["GET"])
def places_get(city_id):
    """
    get places in city if city_id is specified
    """
    city = storage.get(City, city_id)
    if city:
        places = [place for place in city.places]
        return jsonify(places.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=["GET"])
def place_get(place_id):
    """
    Get a place specified by place_id
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.todict())
    else:
        abort(404)


@app_views.route('places/<place_id>', methods=["DELETE"])
def place_delete(place_id):
    """
    delete method handler.
    will delete a place with the specified id.
    """
    place = storage.get(Place, place_id)

    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def place_post(city_id):
    """
    route handler for creating a new city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json():
        return "Not a JSON", 400

    data = request.get_json()
    if 'user_id' not in data.keys():
        return "Missing user_id", 400

    user_id = data.get('user_id')

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    name = data.get('name')
    if not name:
        return "Missing user_id", 400

    new_place = Place(name=name, user_id=user_id,
                      city_id=city_id)

    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def places_put(place_id):
    """
    Returns the Place object with the status code 200
    """
    if not request.is_json:
        return "Not a JSON", 400
    data = request.get_json()
    place = storage.get(Place, place_id)

    if place is None:
        return abort(404)
    if place_id not in data.get('place_id'):
        abort(404)

    for key, value in data.items():
        if key in ('id', 'created_at', 'updated_at', 'user_id', 'city_id'):
            continue
        else:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
    storage.save()
    return jsonify(place.to_dict()), 200
