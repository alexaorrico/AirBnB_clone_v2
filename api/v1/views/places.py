#!/usr/bin/python3
"""place routes"""
from models import storage
from models.city import City
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.user import User


@app_views.route('/cities/<string:city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_cities(city_id):
    """Endpoint to retreive cities"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    all_place = []
    cities = storage.all(City)
    for city in city.places:
        all_place.append(city.to_dict())
    return jsonify(all_place)


@app_views.route('/places/<string:place_id>',
                 strict_slashes=False, methods=['GET'])
def get_city(place_id):
    """retreieves a city by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(place_id):
    """deletes a place object"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def post_city(city_id):
    """creates a new city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description='Missing user_id')
    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data["city_id"] = city_id
    instance = Place(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def put_place(place_id):
    """
    Updates a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
