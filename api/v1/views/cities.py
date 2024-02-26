#!/usr/bin/python3
"""
text
"""
from models import storage
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def states(state_id=None):
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    else:
        if request.methods == 'GET':
            cities = []
            for city in states.cities:
                cities.append(city.to_dict())
            return jsonify(cities)
        elif request.methods == 'POST':
            if request.get_json:
                data = request.get_json
                name = data.get('name')
                if name:
                    new_city = City(**data)
                    setattr(new_city, 'state_id', state_id)
                    storage.save(new_city)
                    return jsonify(new_city.to_dict()), 201
                else:
                    abort(400, 'Missing name')
            else:
                abort(400, 'Not a JSON')


@app_views.route('/cities/<string:city_id>',
                 methods=['GET', 'DELETE'],
                 strict_slashes=False)
def cities(city_id=None):
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    else:
        if request.methods == 'GET':
            return jsonify(cities.to_dict())
        elif request.methods == 'DELETE':
            storage.delete(cities)
            storage.save()
            return {}, 200
