#!/usr/bin/python3
"""
Define route for view Place
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/places/<string:place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/cities/<string:city_id>/places',
                 strict_slashes=False, methods=['GET', 'POST'])
def places(place_id=None, city_id=None):
    """Retrieves a Place or All the places"""
    if request.method == 'GET':
        if place_id is not None:
            place = storage.get(Place, place_id)
            if place is None:
                abort(404)
            return jsonify(place.to_dict())
        elif city_id is no None:
            city = storage.get(City, city_id)
            if city is None:
                abort(404)
            return jsonify(city.places.to_dict())
        places = storage.all(Place)
        places_dicts = [val.to_dict() for val in places.values()]
        return jsonify(places_dicts)

    elif request.method == 'DELETE':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'POST':
        data = request.get_json()
        city = storage.get(City, city_id)
        user = storage.get(User, user_id)
        if city is None:
            abort(404)
        elif not data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        elif 'user_id' not in data:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        elif user is None:
            abort(404)
        elif 'name' not in data:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        else:
            place = Place(**data)
            place.save()
            return make_response(jsonify(place.to_dict()), 201)

    elif request.method == 'PUT':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'not a json'}), 400)

        for key, value in data.items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return make_response(jsonify(place.to_dict()), 200)
