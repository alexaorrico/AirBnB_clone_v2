#!/usr/bin/python3
"""new view for City objects"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET', 'POST'],
    strict_slashes=False
)
def cities(state_id):
    """ GET and POST   """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == "GET":
        cities = list(city.to_dict() for city in state.cities)
        return jsonify(cities)

    if request.method == "POST":
        jreq = request.get_json()
        if jreq is None:
            abort(400, 'Not a JSON')

        if 'name' not in jreq.keys():
            abort(400, 'Missing name')

        jreq['state_id'] = state_id
        city = City(**jreq)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route(
    '/cities/<city_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False
)
def city(city_id):
    """ GET, DELETE, and PUT """

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
        jreq = request.get_json()
        if jreq is None:
            abort(400, 'Not a JSON')

        for k, v in jreq.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict())
