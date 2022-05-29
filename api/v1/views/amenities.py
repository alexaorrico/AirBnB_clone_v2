#!/usr/bin/python3
"""Amenity objects that handles all default RestFul API actions"""

from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities/", methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    amenities_list = []
    for key, value in storage.all("Amenity").items():
        amenities_list.append(value.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a Amenity object """
    estado = storage.get('Amenity', amenity_id)
    if estado:
        return jsonify(estado.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Delete a Amenity object """
    estado = storage.get('Amenity', amenity_id)
    if estado:
        storage.delete(estado)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/amenities/", methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creatte a Amenity object """
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    datos = request.get_json()
    estado = Amenity(**datos)
    storage.new(estado)
    storage.save()
    respuesta = jsonify(estado.to_dict())
    respuesta.status_code = 201
    return respuesta


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Delete a Amenity object """
    if not request.is_json:
        abort(400, "Not a JSON")
    estado = storage.get('Amenity', amenity_id)
    if estado:
        datos = request.get_json()
        if type(datos) is dict:
            omitir = ['id', 'created_at', 'updated_at']
            for name, value in datos.items():
                if name not in omitir:
                    setattr(estado, name, value)
            storage.save()
            return jsonify(estado.to_dict())
    abort(404)
