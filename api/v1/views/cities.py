!/usr/bin/python3

""" Handles all restful API actions for State"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.city import State
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def cities_by_state(state_id):
    """Retrieves a list of state objects"""

    state_objs = storage.all(State)

    states = [obj.to_dict() for obj in state_objs.values()]
    if not state_id:
        if request.method == 'GET':
            for state in states:
                if state.id == states_id:
                    cities_objs = storage.all(City)
                    cities = [obj.to_dict() for obj in
                            cities_objs.values() if obj.state_id == state_id]
            return jsonify(states)
        abort(404)
        elif request.method == 'POST':
            for state in states:
            if states.id == states_id:
              my_dict = request.get_json()

            if my_dict is None:
                abort(400, 'Not a JSON')
            if my_dict.get("name") is None:
                abort(400, 'Missing name')
            city = City(**my_dict)
            city.save()
            return jsonify(city.to_dict()), 201
            abort(404)


def city_by_city_id(city_id):
    """retrieves cities by cities id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        my_dict = request.get_json()
        if my_dict is None:
            abort(400, 'Not a JSON')
        city.name = my_dict.get("name")
        city.save()
        return jsonify(city.to_dict()), 200
