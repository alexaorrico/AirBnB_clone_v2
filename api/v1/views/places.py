#!/usr/bin/python3
"""State objects that handles all default RestFul API actions"""

from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all places in a city objects """
    city = storage.get('City', city_id)
    places_list = []
    if city:
        for value in city.places:
            places_list.append(value.to_dict())
        return jsonify(places_list)
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    lugar = storage.get('Place', place_id)
    if lugar:
        return jsonify(lugar.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Delete a State object """
    objeto = storage.get('Place', place_id)
    if objeto:
        storage.delete(objeto)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places/", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creatte a Place object """
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'name' not in request.json:
        abort(400, "Missing name")
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    datos = request.get_json()
    user_id = datos.get("user_id")
    usuario = storage.get("User", user_id)
    if usuario is None:
        abort(404)
    objeto = Place(**datos)
    objeto.city_id = city_id
    storage.save()
    respuesta = jsonify(objeto.to_dict())
    respuesta.status_code = 201
    return respuesta


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Delete a State object """
    if not request.is_json:
        abort(400, "Not a JSON")
    objeto = storage.get('Place', place_id)
    if objeto:
        datos = request.get_json()
        if type(datos) is dict:
            omitir = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for name, value in datos.items():
                if name not in omitir:
                    setattr(objeto, name, value)
            storage.save()
            return jsonify(objeto.to_dict())
    abort(404)
