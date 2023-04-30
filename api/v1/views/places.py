#!/usr/bin/python3

""" this view Handles all restful API actions for Place"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.city import City

@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_by_city(city_id):
    """retrieve places based on city_id"""

    if request.method == 'GET':
        city = storage.get(City, city_id)

            if city:
                places = [place.to_dict() for place in city.places]
                return jsonify(places)
        abort(404)
    elif request.method == 'POST':
        city = storage.get(City, city_id)
            if city:
                # places = [place.to_dict() for place in city.places]
                my_dict = request.get_json()
                if my_dict is None:
                    abort(400, 'Not a JSON')
                if my_dict.get("user_id") is None:
                    abort(400, 'Missing user_id')
                if my_dict.get("name") is None:
                    abort("400, missing name")

                user = storage.get(user, my_dict.get("user_id"))

                if user:
                    place = place(**my_dict)
                    place.save()
                    return jsonify(place.to_dict()), 201
                abort(404)
            abort(404)


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def place_by_place_id(place_id):
    """ """
    place = storage.get(place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
    elif request.method == 'PUT':
        my_dict = request.get_json()
        if my_dict is None:
            abort(400, 'Not a JSON')
        place.name = my_dict.get("name")
        place.save()
        return jsonify(place.to_dict()), 200
