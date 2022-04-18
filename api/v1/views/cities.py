#!/usr/bin/python3
"""
Creating new view for State object
that handles all default RestFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def state_city(state_id):
    """
    function to retrieve list of all cities connected to states
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = []
    all_cities = storage.all("City")
    for k, v in all_cities.items():
        if v.state_id == str(state_id):
            cities.append(v.to_dict())
    return (jsonify(cities), 200)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def city_all(city_id):
    """
    get cities by id
    """
    ct = storage.get("City", city_id)
    if ct is None:
        abort(404)
    return (jsonify(ct.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_cities(city_id):
    """
    function to delete city based on id
    """
    try:
        del_city = storage.all("City").values()
        obj = [obje.to_dict() for obje in del_city if obje.id == city_id]
        if obj is None:
            abort(404)
        obj.remove(obj[0])
        for obje in del_city:
            if obje.id == city_id:
                storage.delete(obje)
                storage.save()
        return (jsonify({}), 200)
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def post_cities(state_id):
    """
    function to create a city
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    content = request.get_json()
    if not content:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "name" not in content:
        return (jsonify({"error": "Missing name"}), 400)
    content['state_id'] = state.id
    post_city = City(**content)
    post_city.save()

    return (jsonify(post_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def update_cities(city_id):
    """
    function to update City
    """
    check = ["id", "created_at", "updated_at", "state_id"]

    set_city = storage.get("City", city_id)
    if not set_city:
        abort(404)

    if not request.get_json():
        return (jsonify({"error": "Not a JSON"}), 400)

    content = request.get_json()
    for key, value in content.items():
        if key not in check:
            setattr(set_city, key, value)

    set_city.save()
    return (jsonify(set_city.to_dict()), 200)
