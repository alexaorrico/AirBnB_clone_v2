#!/usr/bin/python3
"""cities"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states/<string:state_id>/cities", methods=["GET"], strict_slashes=False)
def state_to_cities(state_id):
    """returns cities by id"""
    state = storage.get(State, state_id)
    if (state is None):
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return (jsonify(cities))


@app_views.route("/cities/<string:city_id>", methods=["GET"], strict_slashes=False)
def city_names(city_id=None):
    """returns city by name"""
    city_name = storage.get(City, city_id)
    if city_name is None:
        abort(404)
    return jsonify(city_name.to_dict())


@app_views.route("/cities/<string:city_id>", methods=["DELETE"], strict_slashes=False)
def remove_city(city_id):
    """Delete city by id"""
    deletes = storage.get(City, city_id)
    if deletes is None:
        abort(404)
    else:
        deletes.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route("states/<string:state_id/cities", methods=["POST"], strict_slashes=False)
def post_city(state_id):
    """makes a state obj"""
    posts = request.get_json()
    if posts is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    new_state = storage.get(State, state_id)
    if new_state is None:
        abort(404)
    if 'name' not in posts:
        return (jsonify({'error': 'Missing name'}), 400)
    if (type(posts) is dict):
        posts['state_id'] = state_id
        obj = City(**posts)
        storage.new(obj)
        storage.save()

        return (jsonify(obj.to_dict()), 201)


@app_views.route("/cities/<city_id", methods=['PUT'], strict_slashes=False)
def amend_city(city_id):
    """update state"""
    update = request.get_json()
    if update is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    new_city = storage.get(City, city_id)
    if new_city is None:
        abort(404)
    else:
        keys = ['id', 'state_at', 'created_at', 'updated_at']
        for key, value in update.items():
            if key not in keys:
                setattr(new_city, key, value)
            else:
                pass
            storage.save()
            return (jsonify(new_city.to_dict()),200)