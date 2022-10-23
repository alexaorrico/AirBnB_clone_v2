#!/usr/bin/python3
""" return dict repersantation of object """
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.base_model import BaseModel
from models.state import State
from models.city import City

@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def city_get(state_id):
    result = []
    """ get all the city objects in a state """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    for i in state.cities:
            result.append(i.to_dict())
    return jsonify(result)

@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city_specific(city_id):
    """ get the specific object from city """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
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


@app_views.route("/states/<state_id>/cities", methods=['POST'], strict_slashes=False)
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


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_specific_put(city_id):
    """ update the specific object from city with city_id """
    instance = None
    if not request.json:
        return make_response("Not a JSON", 400)
    check = ["id", "created_at", "updated_at", "state_id"]
    for i in storage.all("City").values():
        if i.id == city_id:
            instance = i
            for key, value in request.json.items():
                if key not in check:
                    setattr(i, key, value)
                    i.save()
    if not instance:
        abort(404)
    return instance.to_dict(), 200