#!/usr/bin/python3

from models.base_model import *
from api.v1.views import app_views
from models import storage
from models.city import *
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['GET', 'POST'])
def cities_by_state(state_id):
    states = storage.all('State')
    cities = storage.all('City')
    ls = []
    for key, value in states.items():
        if state_id == value.id:
            for key2, value2 in cities.items():
                if value2.state_id == state_id:
                    ls.append(value2.to_dict())
            if request.method == "GET":
                return jsonify(ls)
            elif request.method == "POST":
                if not request.json:
                    return make_response(jsonify({'error': "Not a JSON"}), 400)
                elif not 'name' in request.json:
                    return make_response(jsonify({'error': "Missing name"}), 400)
                else:
                    json = request.json
                    json['state_id'] = state_id
                    new = City(**json)
                    new.save()
                    return make_response(new.to_dict(), 201)
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def city(city_id):
    cities = storage.all('City')
    for key, value in cities.items():
        if city_id == value.id:
            if request.method == "GET":
                return value.to_dict()
            elif request.method == "DELETE":
                storage.delete(value)
                storage.save()
                return {}
            elif request.method == "PUT":
                if not request.json:
                    return make_response(jsonify({'error': "Not a JSON"}), 400)
                else:
                    json = request.json
                    print("json:", json)
                    for key2, value2 in json.items():
                        if key2 != 'id' and key2 != 'state_id' and key2 != 'created_at' and key2 != "updated_at":
                            setattr(value, key2, value2)
                    value.updated_at = datetime.utcnow()
                    storage.save()
                    return make_response(value.to_dict(), 200)
    abort(404)
