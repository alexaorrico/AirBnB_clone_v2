#!/usr/bin/python3
"""Routes Places """
from flask import request, abort, jsonify
from api.v1.app import *
from api.v1.views import app_views
from models import storage, City, Place,State
from api.v1.views.cities import get_state_and_city


def validate(cls, place_id):
    """ validate if query have id to reference """
    try:
        valid = storage.get(cls, place_id)
        valid.to_dict()
    except Exception:
        abort(404)
    return valid


def get_places(city_id, place_id):
    """ get all places """
    if (place_id is not None):
        get_place = validate(Place, place_id).to_dict()
        return jsonify(get_place)
    city = storage.get(City, city_id)
    try:
        all_places = city.places
    except Exception:
        abort(404)
    places = []
    for place in all_places:
        places.append(place.to_dict())
    return jsonify(places)


def delete_place(place_id):
    """ delete place request """
    place = validate(Place, place_id)
    storage.delete(place)
    storage.save()
    response = {}
    return jsonify(response)


def create_place(request, city_id):
    """ create place """
    validate(City, city_id)
    request_json = request.get_json()
    if (request_json is None):
        abort(400, 'Not a JSON')
    try:
        user_id = request_json['user_id']
    except KeyError:
        abort(400, "Missing user_id")
    validate(User, user_id)
    try:
        place_name = body_request['name']
    except KeyError:
        abort(400, "Missing name")
    place = Place(name=place_name, city_id=city_id, user_id=user_id)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict())


def update_place(place_id, request):
    """ update place """
    get_place = validate(Place, place_id)
    request_json = request.get_json()
    if (request_json is None):
        abort(400, 'Not a JSON')
    for key, value in request_json.items():
        if (key not in ('id', 'created_at', 'updated_at')):
            setattr(get_place, key, value)
        storage.save()
        return jsonify(get_place.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 defaults={'place_id': None}, strict_slashes=False)
@app_views.route('/places/<place_id>', defaults={'city_id': None},
                 methods=['GET', 'DELETE', 'PUT'])
def places(city_id, place_id):
    """ Switch to select function """
    if (request.method == "GET"):
        return get_places(city_id, place_id)
    elif request.method == "DELETE":
        return delete_place(place_id)
    elif request.method == "POST":
        return create_place(request, city_id), 201
    elif request.method == 'PUT':
        return update_place(place_id, request), 200