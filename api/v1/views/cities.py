#!/usr/bin/python3
""" Task8 :City objects  """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage, city, state


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ Retrieves the list of all City objects of a State"""
    s_state = storage.get(state.State, state_id)
    if s_state is None:
        abort(404)
    cities = [c.to_dict() for c in s_state.cities]
    return (jsonify(cities), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object:  """
    cities = storage.all(city.City).values()
    for one_city in cities:
        if one_city.id == city_id:
            storage.delete(one_city)
            storage.save()
            return(jsonify({}))
    abort(404)


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ Updates a City object """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    one_city = storage.get(city.City, city_id)
    if one_city is None:
        abort(404)
    setattr(one_city, 'name', content['name'])
    storage.save()
    return(jsonify(one_city.to_dict()), 200)
