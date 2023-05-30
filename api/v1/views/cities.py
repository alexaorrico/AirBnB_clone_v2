#!/usr/bin/python3
"""City module """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities')
def all_cities(state_id):
    """Returns a list of cities"""
    if not storage.get("State", state_id):
        abort(404)

    all_cities = []
    cities = storage.get("State", state_id).cities
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>')
def get_method_city(city_id):
    """Returns a City"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_method_city(city_id):
    """deletes city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete()
    storage.save()
    return make_response(jsonify({}, 200))


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """creates a city"""

    if not request.get_json():
        return make_reponse(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in request.get_json():
        return make_reposnse(jsonify({"error": "Missing name"}), 400)

    city = City()
    city.name = request.get_json().get('name')
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_method_cities(city_id):
    """updates city method"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(city, key, value)

    storage.save()
    return make_response(jsonify(city.to_dict(), 200))
