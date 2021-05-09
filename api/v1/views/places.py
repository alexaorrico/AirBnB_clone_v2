#!/usr/bin/python3
"""
    This is the places page handler for Flask.
"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request

from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<id>/places', methods=['GET', 'POST'])
def cities_id_places(id):
    """
        Flask route at /cities/<id>/places.
    """
    city = storage.get(City, id)
    if (city):
        if request.method == 'POST':
            try:
                kwargs = request.get_json()
            except:
                return {"error": "Not a JSON"}, 400
            if "user_id" not in kwargs:
                return {"error": "Missing user_id"}, 400

            user = storage.get(User, kwargs.get("user_id", None))
            if (user):
                if "name" not in kwargs:
                    return {"error": "Missing name"}, 400
                new_place = Place(city_id=id, **kwargs)
                new_place.save()
                return new_place.to_dict(), 201

        elif request.method == 'GET':
            return jsonify([p.to_dict() for p in city.places])
    abort(404)


@app_views.route('/places/<id>', methods=['GET', 'DELETE', 'PUT'])
def places_id(id):
    """
        Flask route at /places/<id>.
    """
    place = storage.get(Place, id)
    if (place):
        if request.method == 'DELETE':
            place.delete()
            storage.save()
            return {}, 200

        elif request.method == 'PUT':
            try:
                kwargs = request.get_json()
            except:
                return {"error": "Not a JSON"}, 400
            for k, v in kwargs.items():
                if k not in ["id", "user_id", "city_id",
                             "created_at", "updated_at"]:
                    setattr(place, k, v)
            place.save()
        return place.to_dict()
    abort(404)
