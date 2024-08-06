#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models.place import Place
from models.user import User
from models import storage
CT = '/cities/<city_id>/places'
PL = '/places/<place_id>'


@app_views.route(CT, methods=['GET'], strict_slashes=False)
def get_places_from_city(city_id):
    """ """
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    return jsonify([place.to_dict() for place in cities.places])


@app_views.route(PL, methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(CT, methods=['POST'], strict_slashes=False)
def create_place_for_city(city_id):
    """ """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")

    if "user_id" not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if "name" not in data:
        abort(400, description="Missing name")

    data['city_id'] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route(PL, methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, "Not a json")

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route(PL, methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200
