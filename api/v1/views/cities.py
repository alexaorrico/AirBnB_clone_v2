#!/usr/bin/python3
"""Module cities.py: contains cities information"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def cities(state_id):
    """displays and creates a city"""
    if request.method == 'POST':
        res = request.get_json()
        if res is None:
            abort(400, description='Not a JSON')
        if 'name' not in res.keys():
            abort(400, description='Missing name')

        for state in storage.all(State).values():
            if state.id == state_id:
                res['state_id'] = state_id
                new_city = City(**res)
                new_city.save()
                return jsonify(new_city.to_dict()), 201
        abort(404)

    city = [v.to_dict() for k, v in storage.all(City).items()
            if v.state_id == state_id]
    return jsonify(city)


@app_views.route('cities/<city_id>',
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def city(city_id):
    """returns a city based on it's id"""
    for city in storage.all(City).values():
        if city.id == city_id:

            if request.method == 'DELETE':
                city.delete()
                storage.save()
                return '{}'

            elif request.method == 'PUT':
                res = request.get_json()
                if res is None:
                    abort(400, description='Not a JSON')
                for k, v in res.items():
                    if k.endswith('ed_at') or k == 'state_id' or k == 'id':
                        continue
                    setattr(city, k, v)
                city.save()

            return jsonify(city.to_dict())

    abort(404)
