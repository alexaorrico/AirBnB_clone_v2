#!/usr/bin/python
"""holds class City"""
from models.state import State
from models.city import City
from flask import abort
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from os import getenv
from models import storage


#app = Flask(__name__)
#app.register_blueprint(app_views, url_prefix="/api/v1")
#cities = storage.all(City).values()


@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=['GET'])
def all_cities(state_id):
    """grab all cities in a state"""
    print(state_id)
    return jsonify([cD.to_dict() for cD in storage.get("State", state_id).cities])


@app_views.route("cities/<city_id>")
def get_city_obj(city_id):
    """retrieve city obj"""
    obj = [city.to_dict() for city in cities if city.id == city_id]
    if len(obj) == 0:
        abort(404)
    return jsonify(obj)


@app_views.route("cities/<city_id>", strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """delete a city"""
    obj = storage.get("City", city_id)
    print(obj)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


#@app_views.route("states/<state_id>/cities",
#                 strict_slashes=False,
#                 methods=['POST'])
