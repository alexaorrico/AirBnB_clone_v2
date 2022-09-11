#!/usr/bin/python3
"""adasda"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getPlace(city_id):
    """aaasdasdasd"""
    places = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def getPlaceById(place_id):
    """asdasdasda"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place = place.to_dict()
    return jsonify(place)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id):
    """asdasdasda"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def CreatePlace(city_id):
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    if json_req.get("name") is None:
        abort(400, 'Missing name')
    if "user_id" not in request.get_json():
        abort(400, 'Missing user_id')
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    user = storage.get(User, json_req['user_id'])
    if user is None:
        abort(404)
    json_req['city_id'] = city.id
    json_req['user_id'] = user.id
    new_obj = Place(**json_req)
    new_obj.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def updatePlace(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    for key, value in json_req.items():
        if key not in ["id", "created_at", "updated_at", "city_id"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
