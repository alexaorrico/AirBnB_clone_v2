#!/usr/bin/python3
"""City module (Explain use)"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities(state_id=None):
    """ GET status exit 200 if its ok """

    data = storage.get(State, state_id)
    if data is None:
        abort(404)

    if data:
        cities = [xd.to_dict() for xd in data.cities]
        return (jsonify(cities), 200)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def citie(city_id=None):

    data = storage.get(City, city_id)
    if data:
        return jsonify(data.to_dict()), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    """
    delete state if id is match with obj
    """
    if storage.get(City, city_id):
        storage.delete(storage.get(City, city_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_cities(state_id=None):
    """
    POST cities, exit with status 201
    """

    cit_dict = request.get_json()

    obj = storage.get(State, state_id)

    if obj is None:
        abort(404)
    if cit_dict is None:
        abort(400, "Not a JSON")
    if "name" not in cit_dict.keys():
        abort(400, "Missing name")

    cit_dict["state_id"] = state_id
    new_city = City(**cit_dict)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_cities(city_id=None):
    """
    arreglar hohohohohho
    """

    data = request.get_json()

    obj = storage.get(City, city_id)

    if obj is None:
        abort(404)

    if data is None:
        return "Not a JSON", 400

    for k, v in data.items():
        if k in ["id", "created_at", "updated_at"]:
            pass
        else:
            setattr(obj, k, v)
    storage.save()

    return jsonify(obj.to_dict()), 200
