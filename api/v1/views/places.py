#!/usr/bin/python3
"""states module"""
from api.v1.views import app_views
from flask import jsonify, Flask, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from models.city import City


@app_views.route("cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def all_place_by_id(city_id):
    """return json"""
    place_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def all_place(place_id):
    """return json"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_place_by_id(place_id):
    """return json"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(Place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """return json"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    city = request.get_json()
    user = storage.get(User, city['user_id'])

    if not user:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    city["city_id"] = city_id
    ct = Place(**city)
    ct.save()
    return make_response(jsonify(ct.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def put_place_by_id(place_id):
    """return json"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'ccity_id', 'state_id',
                       'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
