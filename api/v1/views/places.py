#!/usr/bin/python3
"""creates a new view for City that handles all Rest Api actions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place


@app_views.route('cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
@app_views.route('places/<place_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def handle_city(city_id=None, place_id=None):
    """Retrieves the list of all city objects by state"""
    if city_id:
        # uses the '/states/<state_it>/cities routes
        city = storage.get(City, city_id)
        if not state:
            abort(404)
        else:
            if request.method == 'GET':
                place_list = []
                for place in city.places:
                    place_list.append(place.to_dict())
                return jsonify(place_list)
            elif request.method == 'POST':
                data = request.get_json()
                if not data:
                    abort(400, 'Not a JSON')
                if not data.get('user_id'):
                    abort(400, 'Missing user_id')
                if not storage.get(User, data.get('user_id')):
                    abort(404)
                if not data.get('name'):
                    abort(400, 'Missing name')
                data["city_id"] = city_id
                new_obj = Place(**data)
                new_obj.save()
                return jsonify(new_obj.to_dict()), 201

    if place_id:
        # uses the '/cities/<city_id>' route
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        else:
            if request.method == 'GET':
                return jsonify(place.to_dict())
            elif request.method == 'DELETE':
                storage.delete(place)
                storage.save()
                return jsonify({}), 200
            elif request.method == 'PUT':
                ignore_keys = ["id", "user_id", "city_id",
                               "created_at", "updated_at"]
                data = request.get_json()
                if not data:
                    abort(400, 'Not a JSON')
                for key in data.keys():
                    if key not in ignore_keys:
                        place[key] = data.get(key)
                place.save()
                return jsonify(city.to_dict()), 200
