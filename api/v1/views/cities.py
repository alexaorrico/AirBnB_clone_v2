#!/usr/bin/python3
"""new view for City objects that handles all
default RestFul API actions
"""
from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route(
    "/states/<state_id>/cities", methods=['GET'], strict_slashes=False)
def cities_view(state_id):
    """
    Retrieves the list of all State objects
    """
    st = storage.get(State, state_id)
    if st is None:
        abort(404)
    cits = [value.to_dict() for value in st.cities]
    return jsonify(cits)


@app_views.route("cities/<city_id>", methods=['GET'], strict_slashes=False)
def city_view(city_id):
    """Retrieves a City object"""
    ct = storage.get(City, city_id)
    if ct is None:
        abort(404)
    return jsonify(ct.to_dict())


@app_views.route(
    "/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    ct = storage.get(City, city_id)
    if st is None:
        abort(404)
    storage.delete(ct)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    "/states/<state_id>/cities", methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Creates a City"""
    content = request.get_json()
    if content:
        st = storage.get(State, state_id)
        if st is None:
            abort(404)
        if content.get('name'):
            new_city = City(**content)
            new_city.state_id = state_id
            new_city.save()
            return jsonify(new_city.to_dict()), 201
        abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    ct = storage.get(City, city_id)
    if ct is None:
        abort(404)
    else:
        content = request.get_json()
        if content:
            keys_ignored = ['id', 'created_at', 'updated_at', "state_id"]
            for key, value in content.items():
                if key not in keys_ignored:
                    setattr(ct, key, value)
            ct.save()
            return jsonify(ct.to_dict()), 200
        else:
            abort(400, "Not a JSON")
