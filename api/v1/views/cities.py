#!/usr/bin/python3
from flask import Flask, Blueprint, jsonify
from flask import abort, request
from models import storage
from api.v1.views import app_views
from models.engine.db_storage import classes

"""
Retrieves the list of all City objects of a State
"""
@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=["GET"])
def get_cities(state_id):
    """Retrieves the list of all City objects of a State
    
    Keyword arguments:
    argument:
        state_id: The ID of the state.
    Return: A JSON response containing a list
        of all cities for the specified state
    Raises:
        404: If the state with the specified ID does not exist.
    """
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)
    
    cities_list = []
    for c in state.cities:
        cities_list.append(c.to_dict())
    return jsonify(cities_list)


@app_views.route("cities/<city_id>", strict_slashes=False, methods=["GET"])
def get_city(city_id):
    """Retrieves a City object.
    
    Keyword arguments:
    city_id -- The ID of the city to retrieve.
    Return: A JSON response containing the details of the specified city.
    Raises:
        404: If the city with the specified ID does not exist.
    """
    city = storage.get(classes["City"], city_id)
    if city in None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete_city(city_id):
    """Deletes a City object
    
    Keyword arguments:
    city_id -- the specified city id to delete
    Return: An empty JSON response.
    Raises:
        404:f the city_id is not linked to any City object
    """
    city = storage.get(classes["City"], city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route("states/<state_id>/cities", strict_slashes=False, methods=["POST"])
def post_state(state_id):
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)
    
    city_data = request.get_json(force=True, silent=True)
    if type(city_data) is not dict:
        abort(400, "Not a JSON")
    
    if "name" in city_data:
        city = classes["City"](state_id=state_id, **city_data)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201
    else:
        abort(400, "Missing name")
    

@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def put_city(city_id):
        """sumary_line
        
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        city = storage.get(classes["City"], city_id)
        if city is None:
            abort(404)
        
        city_data = request.get_json(force=True, silent=True)
        if type(city_data) is not dict:
            abort(400, "Not a JSON")
        
        for key, value in city_data.items():
            if key in ["id", "created_at", "updated_at"]:
                continue
            setattr(city, key, value)
        
        storage.save()
        return jsonify(city.to_dict())
    

    

    