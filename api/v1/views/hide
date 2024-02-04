#!/usr/bin/python3
""" This module contains a blue print for a restful API that
    works for city objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


# @app_views.route('/states/<state_id>/cities/', methods=['GET', 'POST'])
@app_views.route(
        '/states/<state_id>/cities',
        methods=['GET', 'POST'], strict_slashes=False
        )
def post_get_city_obj(state_id):
    """ This function contains two http method handler

        GET:
            return the all city objects related to the state_id
        POST:
            create a new city with the state_id given
        """
    if request.method == 'GET':
        state_objects = storage.all(State)
        key = f'State.{state_id}'
        state = state_objects.get(key)
        cities_list = []
        if state:
            for city in state.cities:
                cities_list.append(city.to_dict())
            return jsonify(cities_list)
        else:
            abort(404)
    elif request.method == 'POST':
        if not request.get_json():
            abort(400, "Not a JSON")
        city_dict = request.get_json()
        if "name" not in city_dict:
            abort(400, description="Missing name")
        city_dict["state_id"] = state_id
        new_city = City(**city_dict)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route(
        '/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False
        )
def delete_put_get_city_obj(city_id):
    """ This function contains three http method handler

    GET:
        return the city with the respective city_id
    DELETE:
        delete the city with the respective city_id
    PUT:
        update the city with the respective city_id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    elif request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        city_dict = request.get_json()
        if not city_dict:
            abort(400, description="Not a JSON")
        for key, value in city_dict.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
