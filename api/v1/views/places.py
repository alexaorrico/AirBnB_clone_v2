#!/usr/bin/python3
""" This module contains a blue print for a restful API that
    works for place objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.city import City


# @app_views.route('/states/<state_id>/cities/', methods=['GET', 'POST'])
@app_views.route(
        '/cities/<city_id>/places',
        methods=['GET', 'POST'], strict_slashes=False
        )
def post_get_place_obj(city_id):
    """ This function contains two http method handler

        GET:
            return the all place objects related to the city_id
        POST:
            create a new place with the city_id given
        """
    if request.method == 'GET':
        city_objects = storage.all(City)
        key = f'City.{city_id}'
        city = city_objects.get(key)
        places_list = []
        if city:
            for place in city.places:
                places_list.append(place.to_dict())
            return jsonify(places_list)
        else:
            abort(404)
    elif request.method == 'POST':
        try:
            places_dict = request.get_json()
        except Exception:
            abort(400, description="Not a JSON")
        if "name" not in places_dict:
            abort(400, description="Missing name")
        if "user_id" not in places_dict:
            abort(400, description="Missing user_id")
        user_objects = storage.all(User)
        key = f'User.{places_dict["user_id"]}'
        user = user_objects.get(key)
        if not user:
            abort(404)
        places_dict["city_id"] = city_id
        new_place = Place(**places_dict)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route(
        '/places/<place_id>',
        methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False
        )
def delete_put_get_place_obj(city_id):
    """ This function contains three http method handler

    GET:
        return the place with the respective place_id
    DELETE:
        delete the place with the respective place_id
    PUT:
        update the place with the respective place_id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    elif request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            place_dict = request.get_json()
            const = ["id", "user_id", "updated_at", "created_at", "city_id"]
            for key, value in place_dict.items():
                if key not in const:
                    setattr(place, key, value)
            place.save()
            return jsonify(place.to_dict()), 200
        except Exception:
            abort(400, description="Not a JSON")
