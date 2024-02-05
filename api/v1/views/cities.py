#!/usr/bin/python3
"""
Define route for view City
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models import storage


@app_views.route('/cities/<string:city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/cities', strict_slashes=False, methods=['GET', 'POST'])
def cities(city_id=None):
    """Retrieves a City or All the cities"""
    if request.method == 'GET':
        if city_id is not None:
            city = storage.get(City, city_id)
            if city is None:
                abort(404)
            return jsonify(city.to_dict())
        cities = storage.all(City)
        cities_dicts = [val.to_dict() for val in cities.values()]
        return jsonify(cities_dicts)

    elif request.method == 'DELETE':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        elif 'name' not in data:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        else:
            city = City(**data)
            city.save()
            return make_response(jsonify(city.to_dict()), 201)

    elif request.method == 'PUT':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'not a json'}), 400)

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)
