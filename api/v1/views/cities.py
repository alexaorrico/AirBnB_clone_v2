#!/usr/bin/python3
""" states view class """
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
from flask import jsonify, request, abort, make_response


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False,
                 methods=["GET", "POST"])
def get_cities(state_id=None):
    """get all cities or create a new city object"""
    state = storage.get(State, state_id)
    all_cities = storage.all("City")

    if state is None:
            abort(404)

    if request.method == "GET":
        obj_list = []
        for obj in all_cities.values():
            if state_id == obj.state_id:
                obj_list.append(obj.to_dict())
        return jsonify(obj_list)

    if request.method == "POST":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if request.get_json().get("name") is None:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        city = City(state_id=state_id, **request.get_json())
        city.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def get_city_id(city_id=None):
    """ get certain city"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == "GET":
        return jsonify(city.to_dict())
    if request.method == "DELETE":
        city.delete()
        storage.save()
        return jsonify({})
    if request.method == "PUT":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, val in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, val)
        city.save()
        return jsonify(city.to_dict())
