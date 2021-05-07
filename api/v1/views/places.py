#!/usr/bin/python3
""" Your first endpoint (route) will be to return the status of your API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
import json

@app_views.route("/cities/<city_id>/places/", methods=['GET', 'POST'])
@app_views.route("/cities/<city_id>/places", methods=['GET', 'POST'])
def show_places(city_id):
    """ returns list of places """
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    if request.method == 'GET':
        lista = []
        for place in cities.places:
            lista.append(place.to_dict())
        return jsonify(lista)
    elif request.method == 'POST':
        if request.json:
            new_dict = request.get_json()
            if "user_id" in new_dict.keys():
                users = storage.all(User).values()
                if new_dict['user_id'] in users:
                    if "name" in new_dict.keys():
                        new_place = Place(**new_dict)
                        storage.new(new_place)
                        storage.save()
                        return jsonify(new_place.to_dict()), 201
                    else:
                        abort(400, "Missing name")
                else:
                    abort(404)
            else:
                abort(400, description="Missing user_id")
        else:
            abort(400, description="Not a JSON")

@app_views.route("places/<place_id>/", methods=['GET', 'DELETE', 'PUT'])
@app_views.route("places/<place_id>", methods=['GET', 'DELETE', 'PUT'])
def show_place(place_id):
    """ returns state data """
    if request.method == 'GET':
        places = storage.all(Place).values()
        for place in places:
            if place.id == place_id:
                return jsonify(place.to_dict())
        abort(404)
    elif request.method == 'DELETE':
        places = storage.all(Place).values()
        for place in places:
            if place.id == place_id:
                place.delete()
                storage.save()
                return jsonify({}), 200
        abort(404)
    elif request.method == 'PUT':
        if request.json:
            new_dict = request.get_json()
            places = storage.all(Place).values()
            for place in places:
                if place.id == place_id:
                    place.name = new_dict['name']
                    storage.save()
                    return jsonify(place.to_dict()), 200
            abort(404)
        else:
            abort(400, description="Not a JSON")

