#!/usr/bin/python3
""" API REST for City """
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities')
def cities_all(state_id):
    """ Route return all cities in states referenced id """
    my_state = storage.get('State', state_id)
    try:
        return jsonify(list(map(lambda x: x.to_dict(), my_state.cities)))
    except:
        abort(404)


@app_views.route('/cities/<city_id>')
def cities_id(city_id):
    """ Route return cities with referenced id """
    my_city = storage.get('City', city_id)
    try:
        return jsonify(my_city.to_dict())
    except:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_id(city_id):
    """ Route delete cities with referenced id """
    my_object = storage.get('City', city_id)
    if my_object is not None:
        storage.delete(my_object)
        storage.save()
    else:
        abort(404)
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_cities(state_id):
    """ Route create cities """
    if request.is_json:
        try:
            data = request.get_json()
            if 'name' in data:
                data["state_id"] = state_id
                new_city = City(**data)
                new_city.save()
                return jsonify(new_city.to_dict()), 201
            else:
                return jsonify(error="Missing name"), 400
        except:
            return jsonify(error="Not a JSON"), 400
    else:
        return jsonify(error="Not a JSON"), 400


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_cities(city_id):
    """ Route update cities """

    if request.is_json:
        data = request.get_json()
        my_object = storage.get('City', city_id)
        if my_object is not None:
            for keys, values in data.items():
                if keys not in ["created_at", "updated_at", "id"]:
                    setattr(my_object, keys, values)
            my_object.save()
            return jsonify(my_object.to_dict()), 200
        else:
            abort(404)
    else:
        return jsonify(error="Not a JSON"), 400
