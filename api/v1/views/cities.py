#!/usr/bin/python3
"""creates a new view for City that handles all Rest Api actions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def handle_city(state_id=None, city_id=None):
    """Retrieves the list of all city objects by state"""
    if state_id:
        # uses the '/states/<state_it>/cities routes
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        else:
            if request.method == 'GET':
                city_list = []
                for city in state.cities:
                    city_list.append(city.to_dict())
                return jsonify(city_list)
            elif request.method == 'POST':
                data = request.get_json()
                if not data:
                    abort(400, 'Not a JSON')
                if not data.get('name'):
                    abort(400, 'Missing name')
                data["state_id"] = state_id
                new_obj = City(**data)
                new_obj.save()
                return jsonify(new_obj.to_dict()), 201

    if city_id:
        # uses the '/cities/<city_id>' route
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        else:
            if request.method == 'GET':
                return jsonify(city.to_dict())
            elif request.method == 'DELETE':
                storage.delete(city)
                storage.save()
                return jsonify({}), 200
            elif request.method == 'PUT':
                ignore_keys = ["id", "created_at", "updated_at", "state_id"]
                data = request.get_json()
                if not data:
                    abort(400, 'Not a JSON')
                city.name = data.get('name')
                city.save()
                return jsonify(city.to_dict()), 200
