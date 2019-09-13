#!/usr/bin/python3
"""State objects that handles all default RestFul API actions"""

from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states/", methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves the list of all State objects """
    states_list = []
    for key, value in storage.all("State").items():
        states_list.append(value.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object """
    estado = storage.get('State', state_id)
    if estado:
        return jsonify(estado.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Delete a State object """
    estado = storage.get('State', state_id)
    if estado:
        storage.delete(estado)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states/", methods=['POST'], strict_slashes=False)
def create_state():
    """ Creatte a State object """
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    datos = request.get_json()
    estado = State(**datos)
    storage.new(estado)
    storage.save()
    respuesta = jsonify(estado.to_dict())
    respuesta.status_code = 201
    return respuesta


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Delete a State object """
    if not request.is_json:
        abort(400, "Not a JSON")
    estado = storage.get('State', state_id)
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
