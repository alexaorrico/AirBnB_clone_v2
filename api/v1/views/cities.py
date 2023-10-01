#!/usr/bin/python3
"""script to serve routes related to cities objects"""
from models.state import City
from models.state import State
from models import storage
from api.v1.views import app_views
import json
from flask import request, jsonify, abort

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Retrieves a list of all State objects"""
    cities = storage.all(City)
    list_cities = [city.to_dict() for city in cities.values() if city.state_id == state_id]

    if len(list_cities) == 0:
        abort(404)
    return jsonify(list_cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def server_city_id(city_id):
    """Retrives a State object"""
    response = storage.get(City, city_id)

    if response is None:
        abort(404)

    return jsonify(response.to_dict())

@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city_obj(city_id):
    """deletes a State object"""
    city_to_delete = storage.get(City, city_id)

    if city_to_delete is None:
        abort(404)

    storage.delete(city_to_delete)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_new_city(state_id):
    """creates a State"""

    response = storage.get(State, state_id)

    if response is None:
        abort(404)

    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400, description="Content-Type is not application/json")

    if data_entered.get('name') is None:
        abort(400, description="Missing name")

    # if name not in dict
    if data_entered.get('name') is None:
        abort(400, description="Missing name")

    new_city = City(name=data_entered.get('name'))
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city_obj(city_id):
    """updates a State object"""
    city_to_update = storage.get(City, city_id)

    if city_to_update is None:
        abort(404)

    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400, description="Content-Type is not application/json")

    for key, value in data_entered.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city_to_update, key, value)

    storage.save()

    return jsonify(city_to_update.to_dict()), 200

# all_states = storage.all(State)  # is a dict
# all_cities = storage.all(City)


# @app_views.route("/states/<state_id>/cities", strict_slashes=False)
# def return_cities(state_id):
#     """returns list of cities of a State"""
#     states_cities_list = []  # holds all cities in a given state

#     # forming the key of the State instance -> State.id
#     state_key = "State.{}".format(state_id)
#     # raise error if state_id is not linked to any State object
#     if state_key not in all_states.keys():
#         return jsonify({"error": "Not found"}), 404

#     for key, value in all_cities.items():
#         if state_id == value.state_id:
#             states_cities_list.append(value.to_dict())
#     return json.dumps(states_cities_list)


# @app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
# def serve_city_id(city_id):
#     """Retrives a City object"""
#     # forming the key of the City instance -> City.id
#     city_key = "City.{}".format(city_id)

#     if city_key not in all_cities.keys():
#         return json.dumps({"error": "Not found"}), 404

#     # use the get method that returns an instance based on Cls and id
#     found_city = storage.get(City, city_id)
#     return json.dumps(found_city.to_dict())


# @app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
# def delete_city_obj(city_id):
#     """deletes a City object"""
#     # forming the key of the State instance -> State.id
#     city_key = "City.{}".format(city_id)

#     if city_key not in all_cities.keys():
#         return json.dumps({"error": "Not found"}), 404

#     city_to_delete = all_cities[city_key]  # gives us the instance
#     storage.delete(city_to_delete)
#     return json.dumps({}), 200


# @app_views.route('/states/<state_id>/cities',
#                  methods=['POST'], strict_slashes=False)
# def create_city(state_id):
#     """creates a City object"""
#     # forming the key of the State instance -> State.id
#     state_key = "State.{}".format(state_id)
#     # raise error if state_id is not linked to any State object
#     if state_key not in all_states.keys():
#         return jsonify({"error": "Not found"}), 404

#     data_entered = request.get_json()

#     if data_entered is None:  # if not valid json
#         return "Not a JSON", 400

#     # if name not in dict
#     if data_entered.get('name') is None:
#         return "Missing name", 400
#     new_city = City(name=data_entered.get('name'))
#     return jsonify(new_city.to_dict())


# @app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
# def update_city_obj(city_id):
#     """updates a City object"""
#     # forming the key of the City instance -> City.id
#     city_key = "City.{}".format(city_id)

#     if city_key not in all_cities.keys():
#         return json.dumps({"error": "Not found"}), 404

#     data_entered = request.get_json()  # method returns None if fails
#     if data_entered is None:
#         return "Not a JSON", 400

#     city_to_update = all_cities[city_key]  # gives us the instance

#     # UPDATE THIS. SHOULD CHECK ALL KEY,VALUES ENTERED IN THE POST
#     # REQUEST DICT, THEN USE THAT TO UPDATE THE VALUES
#     # NOT AS DONE BELOW (SHOULD BE DYNAMIC)
#     city_to_update.name = data_entered['name']
#     city_to_update.save()
#     return json.dumps(city_to_update.to_dict()), 200
