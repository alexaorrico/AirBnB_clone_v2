#!/usr/bin/python3
"""handles city route requests"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=[
    'POST', 'GET'])
@app_views.route('/cities/<city_id>', strict_slashes=False, methods=[
    'PUT', 'GET', 'DELETE'])
def cities(state_id=None, city_id=None):
    """retrieves list of all states or state by state_id"""
    if state_id is not None:
        # /states/<state_id>/cities GET method
        if request.method == 'GET':
            states_list = storage.all('State')
            cities_list = []
            if states_list is not {}:
                for state in states_list.values():
                    if state.id == state_id:
                        for city in state.cities:
                            cities_list.append(city.to_dict())
                        return jsonify(cities_list)
            abort(404)

        # /states/<state_id>/cities POST method
        if request.method == 'POST':
            new_json = request.get_json(silent=True)
            state = storage.get(State, state_id)
            if state is None:
                abort(404)
            if new_json is None:
                abort(400, 'Not a JSON')
            if 'name' not in new_json:
                abort(400, 'Missing name')
            new_city = City(**new_json)
            new_city.state_id = state_id
            new_city.save()
            return jsonify(new_city.to_dict()), 201

    else:
        # /cities/<city_id> GET method
        if request.method == 'GET':
            city = storage.get(City, city_id)
            if city is not None:
                return jsonify(city.to_dict())
            abort(404)

        # /cities/<city_id> DELETE method
        if request.method == 'DELETE':
            city = storage.get(City, city_id)
            if city is not None:
                city.delete()
                storage.save()
                return jsonify({}), 200
            abort(404)

        # /cities/<city_id> PUT method
        if request.method == 'PUT':
            city = storage.get(City, city_id)
            if city is None:
                abort(404)
            new_json = request.get_json(silent=True)
            if new_json is None:
                abort(400, 'Not a JSON')
            for k, v in new_json.items():
                if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                    setattr(city, k, v)
            city.save()
            return jsonify(city.to_dict()), 200
