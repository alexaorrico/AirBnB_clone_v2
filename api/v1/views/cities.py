#!/usr/bin/python3
""" Your first endpoint (route) will be to return the status of your API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
import json


@app_views.route("/states/<state_id>/cities/", methods=['GET', 'POST'])
@app_views.route("/states/<state_id>/cities", methods=['GET', 'POST'])
def show_cities(state_id):
    """ returns list of states """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    if request.method == 'GET':
        lista = []
        for city in states.cities:
            lista.append(city.to_dict())
        return jsonify(lista)
    elif request.method == 'POST':
        if request.json:
            new_dict = request.get_json()
            if "name" in new_dict.keys():
                new_city = State(**new_dict)
                storage.new(new_city)
                storage.save()
                return jsonify(new_city.to_dict()), 201
            else:
                abort(400, description="Missing name")
        else:
            abort(400, description="Not a JSON")


@app_views.route("cities/<city_id>/", methods=['GET', 'DELETE', 'PUT'])
@app_views.route("cities/<city_id>", methods=['GET', 'DELETE', 'PUT'])
def show_city(city_id):
    """ returns state data """
    if request.method == 'GET':
        cities = storage.all(City).values()
        for city in cities:
            if city.id == city_id:
                return jsonify(city.to_dict())
        abort(404)
    elif request.method == 'DELETE':
        cities = storage.all(City).values()
        for city in cities:
            if city.id == city_id:
                city.delete()
                storage.save()
                return jsonify({}), 200
        abort(404)
    elif request.method == 'PUT':
        if request.json:
            new_dict = request.get_json()
            cities = storage.all(City).values()
            for city in cities:
                if city.id == city_id:
                    city.name = new_dict['name']
                    storage.save()
                    return jsonify(city.to_dict()), 200
            abort(404)
        else:
            abort(400, description="Not a JSON")
