#!/usr/bin/python3
"""
-------------------
New view for Cities
-------------------
"""
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from api.v1.views.aux_func import aux_func

methods = ["GET", "DELETE", "POST", "PUT"]


@app_views.route("/cities/<city_id>", methods=methods)
def cities_id(city_id):
    """
    ----------------
    Route for cities
    ----------------
    """
    cities = storage.all(City)
    met = request.method
    if met in ["GET", "DELETE"]:
        res = aux_func(City, met, city_id)

    elif met == "PUT":
        if city_id:
            key = "City.{}".format(city_id)
            if key not in cities.keys():
                abort(404)
            else:
                try:
                    data = request.get_json()
                    city = cities[key]
                    for attr, value in data.items():
                        if attr not in ["id", "created_at", "updated_at",
                                        "state_id"]:
                            setattr(city, attr, value)
                    # No sabemos si hay que guardar
                    storage.save()
                    return jsonify(city.to_dict()), 200, {'Content-Type':
                                                          'application/json'}
                except Exception as err:
                    return jsonify("Not a JSON"), 400, {'Content-Type':
                                                        'application/json'}
    return res


@app_views.route("/states/<state_id>/cities", methods=methods)
def cities_by_state(state_id=None):
    """
    ----------------------------------
    Retrieve a list of cities by state
    ----------------------------------
    """
    state_obj = storage.get(State, state_id)
    if request.method == 'GET':
        if state_obj:
            cities = [city.to_dict() for city in state_obj.cities]
            return jsonify(cities), 200, {'Content-Type':
                                          'application/json'}
        else:
            abort(404)
    elif request.method == 'POST':
        city_data = request.get_json()
        if not city_data:
            return jsonify("Not a JSON"), 400, {'Content-Type':
                                                'application/json'}
        elif not state_obj:
            abort(404)
        elif "name" not in city_data.keys():
            return jsonify("Missing name"), 400, {'Content-Type':
                                                  'application/json'}
        else:
            new_city = City(**city_data)
            # No sabemos si hay que guardar
            new_city.save()
            return jsonify(new_city.to_dict()), 201, {'Content-Type':
                                                      'application/json'}
