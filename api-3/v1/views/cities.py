#!/usr/bin/python3
"""This is module cities"""
from api.v1.views import (
    app_views,
    storage)
from flask import (
    abort,
    jsonify,
    request
)
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def state_all_cities(state_id):
    """Example endpoint returning a list of all the cities of a state
    Retrieves all the cities of a given state_id
    ---
    parameters:
      - name: state_id
        in: path
        type: string
        enum: ['None', '10098698-bace-4bfb-8c0a-6bae0f7f5b8f']
        required: true
        default: None
    definitions:
      City:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          id:
            type: string
            description: the id of the city
          name:
            type: string
            description: name of the city
          state_id:
            type: string
            description: the id of the state
          updated_at:
            type: string
            description: The date the object was updated
    responses:
      200:
        description: A list of dictionaries of city object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = [city.to_dict() for city in state.cities]
    return jsonify(all_cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def one_city(city_id):
    """Example endpoint returning one city
    Retrieves one city of a given city_id
    ---
    parameters:
      - name: city_id
        in: path
        type: string
        enum: ['None', '1da255c0-f023-4779-8134-2b1b40f87683']
        required: true
        default: None
    definitions:
      City:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          id:
            type: string
            description: the id of the city
          name:
            type: string
            description: name of the city
          state_id:
            type: string
            description: the id of the state
          updated_at:
            type: string
            description: The date the object was updated
    responses:
      200:
        description: A list of a dictionary of a city object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_one_city(city_id):
    """Example endpoint deleting one city
    Deletes a state based on the city_id
    ---
    definitions:
      City:
        type: object

    responses:
      200:
        description: An empty dictionary
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_one_city(state_id):
    """Example endpoint creating one city
    Creates one city tied with the given state_id based on the JSON body
    ---
    parameters:
      - name: city_id
        in: path
        type: string
        enum: ['None', '10098698-bace-4bfb-8c0a-6bae0f7f5b8f']
        required: true
        default: None
    definitions:
      City:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          id:
            type: string
            description: the id of the city
          name:
            type: string
            description: name of the city
          state_id:
            type: string
            description: the id of the state
          updated_at:
            type: string
            description: The date the object was updated
    responses:
      201:
        description: A list of a dictionary of a city object
    """
    try:
        r = request.get_json()
    except Exception:
        r = None
    if r is None:
        return "Not a JSON", 400
    if 'name' not in r.keys():
        return "Missing name", 400
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    # creates the dictionary r as kwargs to create a city object
    c = City(**r)
    c.state_id = state_id
    c.save()
    return jsonify(c.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_one_city(city_id):
    """Example endpoint updates one city
    Updates one city tied with the given state_id based on the JSON body
    ---
    parameters:
      - name: city_id
        in: path
        type: string
        enum: ['None', "1da255c0-f023-4779-8134-2b1b40f87683"]
        required: true
        default: None
    definitions:
      City:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          id:
            type: string
            description: the id of the city
          name:
            type: string
            description: name of the city
          state_id:
            type: string
            description: the id of the state
          updated_at:
            type: string
            description: The date the object was updateS
    responses:
      200:
        description: A list of a dictionary of a city object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    try:
        r = request.get_json()
    except Exception:
        r = None
    if r is None:
        return "Not a JSON", 400
    for k in ("id", "created_at", "updated_at", "state_id"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
