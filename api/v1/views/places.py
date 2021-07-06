#!/usr/bin/python3
"""Places module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route(
    '/cities/<city_id>/places',
    methods=['GET'],
    strict_slashes=False)
@app_views.route(
    '/places/<place_id>',
    methods=['GET'],
    strict_slashes=False)
def placeof_city(city_id=None, place_id=None):
    """place and cities"""
    if place_id:
        if storage.get(Place, place_id):
            return jsonify(storage.get(Place, place_id).to_dict())
        else:
            abort(404)
    if city_id:
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        list_places = []
        for place in city.places:
            list_places.append(place.to_dict())
        return jsonify(list_places)
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """
    delete place if id is match with obj_place
    """
    if storage.get(Place, place_id):
        storage.delete(storage.get(Place, place_id))
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def post_place(city_id=None):
    """
    post method to place
    """
    city = storage.get(City, city_id)
    if city:
        place = request.get_json()
        if not place:
            abort(400, "Not a JSON")
        if "user_id" not in place:
            abort(400, "Missing user_id")
        if not storage.get("User", place["user_id"]):
            abort(404)
        if "name" not in place:
            abort(400, "Missing name")
        else:
            place['city_id'] = city.id
            new_place = Place(**place)
            storage.new(new_place)
            storage.save()
            return jsonify(new_place.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id=None):
    """
    arreglar
    """

    data = request.get_json()

    obj = storage.get(Place, place_id)

    if obj is None:
        abort(404)

    if data is None:
        return "Not a JSON", 400

    for k, v in data.items():
        if k in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            pass
        else:
            setattr(obj, k, v)
    storage.save()

    return jsonify(obj.to_dict()), 200
