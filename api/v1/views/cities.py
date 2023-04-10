#!/usr/bin/python3

from flask import abort, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_list(state_id):
    """returns citys for a state given"""

    from models import storage
    from models.state import State

    state_found = storage.get(State, state_id)
    if state_found == None:
        abort(404)

    list_of_cities = state_found.cities
    citys_dict = []

    for city in list_of_cities:
        citys_dict.append(city.to_dict())

    return jsonify(citys_dict)


@app_views.route('/cities/<city_id>', methods=['GET'])
def cities(city_id):
    """returns city of id given"""

    from models import storage
    from models.city import City

    city_found = storage.get(City, city_id)
    if city_found == None:
        abort(404)

    return jsonify(city_found.to_dict()), 201


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """create a city and links to state"""
    from flask import request
    from models.city import City

    http_request = request.get_json(silent=True)
    if http_request == None:
        return 'Not a JSON', 400
    elif 'name' not in http_request.keys():
        return 'Missing name', 400

    new_city = City(**http_request)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """updates given city"""

    from flask import request
    from models.city import City

    found_city = storage.get(City, city_id)

    if found_city == None:
        return '', 404

    http_request = request.get_json(silent=True)
    if http_request == None:
        return 'Not a JSON', 400

    for key, values in http_request.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(found_city, key, values)

    storage.save()
    return jsonify(found_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id):
    """DELETE city if id is found"""

    from models import storage
    from models.city import City

    city_found = storage.get(City, city_id)
    if city_found == None:
        return '{}', 404

    storage.delete(city_found)
    storage.save()
    return jsonify({}), 200
