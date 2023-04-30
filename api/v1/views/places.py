#!/usr/bin/python3
"""creates a new view for Places that handles all Rest Api actions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def handle_place(city_id=None, place_id=None):
    """Retrieves the list of all place objects by city"""
    if city_id:
        # uses the '/cities/<city_id>/places routes
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        else:
            if request.method == 'GET':
                place_list = []
                for places in city.places:
                    place_list.append(places.to_dict())
                return jsonify(place_list)
            elif request.method == 'POST':
                data = request.get_json()
                if not data:
                    abort(400, 'Not a JSON')
                if not data.get('user_id'):
                    abort(400, 'Missing user_id')
                user_id = storage.get(User, data.get('user_id'))
                if not user_id:
                    abort(404)
                if not data.get('name'):
                    abort(400, 'Missing name')
                data["city_id"] = city_id
                new_obj = Place(**data)
                new_obj.save()
                return jsonify(new_obj.to_dict()), 201

    if place_id:
        # uses the '/places/<place_id>' route
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
                ignore_keys = ["id", "created_at", "updated_at", "user_id",
                               "city_id"]
                data = request.get_json()
                if not data:
                    abort(400, 'Not a JSON')
                for key, value in data.items():
                    if key in ignore_keys:
                        continue
                    setattr(place, key, value)
                place.save()
                return jsonify(place.to_dict()), 200
