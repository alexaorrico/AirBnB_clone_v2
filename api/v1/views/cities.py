#!/usr/bin/python3
"""
file for "/api/v1/states" API
with GET, POST, PUT and DELETE
for getting, posting, putting and deleting
State objects in 'storage', imported from
'models', and saving those changes in the
'storage's database/JSON file.
"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response

@app_views.route(
    "/states/<state_id>/cities",
    strict_slashes=False,
    methods=["GET"]
    )
def get_cities(state_id):
    """ module to get cities in states"""
    state = storage.get(State, state_id)
    if state in None:
        return abort(404)
    cities = state.cities
    city_list = []
    for city in cities:
        city_list.append(city.to_dict())
    return jsonify(cities.to_dict())


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_cities(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    return jsonify(city.to_dict())


@app_views.route(
        "/states//<state_id>/cities",
        strict_slashes=False,
        methods=["POST"]
    )
def create_new_city(state_id):
    state = State.get(State, state_id)
    if state is None:
        abort(404)
    new_city_JSON = request.get_json()
    if 'name' not in new_city_JSON:
        abort(400, "Missing name")
    new_city_JSON['state_id'] = state_id
    new_city = City(**new_city_JSON)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route(
    "/cities/<city_id>",
    strict_slashes=False,
    methods=["DELETE"]
    )
def delete_city(city_id):
    """
    Deletes city object with 'city_id' as its 'id'
    field/column value (let's call it 'target')
    from 'storage.all' dictionary, by calling storage.delete(<target>)

    Returns ({}, 200) if successful,
    404 if 'target' doesn't exist.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}, 200 )


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_city(city_id):
    """Update a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)

if __name__ == "__main__":
    app_views.run(host='0.0.0.0')
