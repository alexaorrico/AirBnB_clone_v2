#!/usr/bin/python3
"""
New view for CIty objects that handles taht handles all default ResFul API.
"""


from flask import abort
from flask import jsonify
from models.city import City
from models import storage
from flask import Flask
from api.v1.views import app_views
from flask import request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city(state_id):
    """
    """
    if state_id is None:
        abort(404)
    city_list = []
    if storage.get('State', state_id) is None:
        abort(404)
    get_cities = storage.all("City")
    for key, value in get_cities.items():
        if value.state_id == state_id:
            city_list.append(value.to_dict())
    return jsonify(city_list)


@app_views.route("/cities/<city_id>", methods=['GET'],
                 strict_slashes=False)
def get_city_id(city_id):
    """
    Return id of the function
    """
    cityArr = storage.get("City", city_id)
    if cityArr is None:
        abort(404)
    return jsonify(cityArr.to_dict())


@app_views.route("cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def get_city_delete(city_id):
    """
    method Delete of the function
    """
    cityArr = storage.get('City', city_id)
    if cityArr is None:
        abort(404)
    else:
        storage.delete(cityArr)
        storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def set_city_POST(state_id):
    """
    State object
    """
    state = storage.get("State", state_id)
    info = request.get_json()
    if state is None:
        abort(400)
    if not info:
        abort((400), "Not a JSON")
    elif 'name' not in info:
        abort((400), "Missing name")
    else:
        info["state_id"] = state_id
        city_post = City(**info)
        storage.new(city_post)
        storage.save()
        new_city = storage.get("City", city_post.id)
        return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def set_city_PUT(city_id):
    """
    method PUT
    """
    city_st = storage.get("City", city_id)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if city_st is None:
        abort(404)
    for atriv, val in request.json.items():
        if ((atriv != "id" and atriv != "state_id" and
             atriv != "created_at" and atriv != "updated_at")):
            setattr(city_st, atriv, val)
    storage.save()
    return jsonify(city_st.to_dict()), 200

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
