#!/usr/bin/python3
"""RESTful API for class Place"""

from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def get_places(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def post_place(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    res = request.get_json()
    if not res:
        return abort(400, description="Not a JSON")
    if 'user_id' not in res:
        return abort(400, description="Missing user_id")
    if 'name' not in res:
        return abort(400, description="Missing name")
    user = storage.get(User, res['user_id'])
    if not user:
        return abort(404)
    res['city_id'] = city_id
    new_place = Place(**res)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def put_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    res = request.get_json()
    if not res:
        return abort(400, description="Not a JSON")
    for key, value in res.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

