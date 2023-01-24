#!/usr/bin/python3
"""
Flask route that returns json status response on Places Objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def list_or_create_places(city_id):
    """
    get or create new cities given a city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        places = storage.all(Place)
        return jsonify([place.to_dict() for place in places.values()
                        if place.to_dict().get("city_id") == city_id])
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if data.get("user_id") is None:
            abort(400, "Missing user_id")
        user = storage.get(User, data.get("user_id"))
        if user is None:
            abort(404)
        if data.get("name") is None:
            abort(400, "Missing name")
        data["city_id"] = city_id
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_or_delete_or_update_place(place_id):
    """
    get, delete or update place given a place_id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(
            place.to_dict()
        )
    if request.method == 'DELETE':
        place.delete()
        del place
        return jsonify({}), 200
    if request.method == 'PUT':
        update = request.get_json()
        if update is None:
            abort(400, 'Not a JSON')
        for key, val in update.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(place, key, val)
        place.save()
        return jsonify(place.to_dict()), 200
