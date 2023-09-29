from models.state import City
from models.state import State
from models import storage
from api.v1.views import app_views
import json
from flask import request

all_states = storage.all(State)  # is a dict
all_cities = storage.all(City)


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def return_cities(state_id):
    """returns list of cities of a State"""
    states_cities_list = []  # holds all cities in a given state

    # forming the key of the State instance -> State.id
    state_key = "State.{}".format(state_id)
    # raise error if state_id is not linked to any State object
    if state_key not in all_states.keys():
        return json.dumps({"error": "Not found"}), 404
    
    for key, value in all_cities.items():
        if state_id == value.state_id:
            states_cities_list.append(value.to_dict())
    return json.dumps(states_cities_list)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def serve_city_id(city_id):
    """Retrives a City object"""
    # forming the key of the City instance -> City.id
    city_key = "City.{}".format(city_id)

    if city_key not in all_cities.keys():
        return json.dumps({"error": "Not found"}), 404
    
    # use the get method that returns an instance based on Cls and id
    found_city = storage.get(City, city_id)
    return json.dumps(found_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city_obj(city_id):
    """deletes a City object"""
    # forming the key of the State instance -> State.id
    city_key = "City.{}".format(city_id)

    if city_key not in all_cities.keys():
        return json.dumps({"error": "Not found"}), 404
    
    city_to_delete = all_cities[city_key] # gives us the instance
    storage.delete(city_to_delete)
    return json.dumps({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city_obj(city_id):
    """updates a City object"""
    # forming the key of the City instance -> City.id
    city_key = "City.{}".format(city_id)

    if city_key not in all_cities.keys():
        return json.dumps({"error": "Not found"}), 404
    
    data_entered = request.get_json()  # method returns None if fails
    if data_entered is None:
        return "Not a JSON", 400
    
    city_to_update = all_cities[city_key] # gives us the instance

    # UPDATE THIS. SHOULD CHECK ALL KEY,VALUES ENTERED IN THE POST
    # REQUEST DICT, THEN USE THAT TO UPDATE THE VALUES
    # NOT AS DONE BELOW (SHOULD BE DYNAMIC)
    city_to_update.name = data_entered['name']
    city_to_update.save()
    return json.dumps(city_to_update.to_dict()), 200