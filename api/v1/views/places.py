#!/usr/bin/python3
"""RESTful API action for City object"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.places import Place
from models.state import State
from models import storage


@app_views.route('/cities/<city_id>/places', methods=["GET"])
def places_get(city_id):
    """
    get places in city if city_id is specified
    """
    city = storage.get(City, city_id)
    if city:
        places = [place for place in state.places]
        return jsonify(places.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=["GET"])
def place_get(city_id):
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
    place = storage.get(places, place_id)

    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    else:
        abort(404)


TODO: Start from post
@app_views.route('/cities/<city_id>/places', methods=['POST'])
def place_post(city_id):
    """
    route handler for creating a new city
    """
    if not request.is_json():
        return "Not a JSON", 404

    data = request.get_json()

    if city_id not in :
        abort(404)
    if 'user_id' not in data.keys():
        return "Missing user_id",404

    all_cities = storage.get('Cities').all()
    users = [user.to_dict() for user in all_cities.values() if user.id == user_id]

    if users is None:
        abort(404)

    new_place = Place(name=data.get('name'), user_id=data.get('user_id'),
            city_id=city_id)
    all_users = storage.all('User').values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == new_place.user_id]

    if user_obj is None:
        abort(404)

    places = []
    storage.new(new_place)
    storage.save()
    places.append(new_place.to_dict())
    return jsonify(places[0]), 201

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
