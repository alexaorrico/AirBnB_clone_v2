#!/usr/bin/python3
""" file that handles all cities in flask stuff """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def showCities(state_id):
    """ Shows all cities in the state """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    count_l = []
    eachCity = storage.all("City")
    for value in eachCity.values():
        if value.state_id == state_id:
            count_l.append(value.to_dict())
    return(jsonify(count_l))


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def a_city_id(city_id):
    """ Gets the city and its id that is correlated """
    bayAireUh = storage.get("City", city_id)
    if bayAireUh:
        return jsonify(bayAireUh.to_dict())
    else:
        return (jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=["DELETE"])
def del_city_id(city_id):
    """ deletes the city id """
    thing = storage.all("City")
    muricanCity = "City." + city_id
    town = thing.get(muricanCity)
    if town is None:
        abort(404)
    else:
        town.delete()
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def postCity(state_id):
    """ posts the city """
    if storage.get("State", state_id) is None:
        abort(404)
    thing = request.get_json(silent=True)
    if thing is None or not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)
    city = thing.get("name")
    if city is None:
        return (jsonify({"error": "Missing name"}), 400)
    c = City()
    c.name = city
    c.state_id = state_id
    c.save()
    return (jsonify(c.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=["PUT"])
def updateCity(city_id):
    """ updates the city """
    # garbage = {"id", "created_at", "updated_at"}
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)
    thing = request.get_json()
    for key, value in thing.items():
        if key == 'name':
            setattr(city, key, value)
    city.save()
    return (jsonify(city.to_dict()), 200)
