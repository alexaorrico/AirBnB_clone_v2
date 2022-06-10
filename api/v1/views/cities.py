#!/usr/bin/python3
""" City view """
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def list_cities(state_id):
    """
    Retrieves the list of all City objects of a State
    ---
    tags:
      - City
    parameters:
      - name: state_id
        in: path
        required: true
    responses:
      200:
        description: All cities from a given state
        schema:
          type: array
          items:
            type: object
            properties:
              __class__:
                type: string
              created_at:
                type: string
              id:
                type: string
              name:
                type: string
              state_id:
                type: string
              updated_at:
                type: string
          example:
            [
              {
                "__class__": "City",
                "created_at": "2022-05-31T20:42:53.350872",
                "id": "2805d07b-7c2e-4bb9-ad28-a852f17e52e2",
                "name": "Miami",
                "state_id": "aa95665c-6295-4b5a-8d15-96686e9da62e",
                "updated_at": "2022-05-31T20:42:53.350872"
              },
              {
                "__class__": "City",
                "created_at": "2022-05-31T20:42:53.350872",
                "id": "f94f7d71-4f52-44ae-80ca-12936d27b7b8",
                "name": "Orlando",
                "state_id": "aa95665c-6295-4b5a-8d15-96686e9da62e",
                "updated_at": "2022-05-31T20:42:53.350872"
              }
            ]
      404:
        description: No state found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities(city_id):
    """
    Retrieves a City object
    ---
    tags:
      - City
    parameters:
      - name: city_id
        in: path
        required: true
    responses:
      200:
        description: City found
        schema:
          type: object
          properties:
            __class__:
              type: string
            created_at:
              type: string
            id:
              type: string
            name:
              type: string
            updated_at:
              type: string
          example:
            __class__: "City"
            created_at: "2022-05-31T20:42:53.350872"
            id: "f94f7d71-4f52-44ae-80ca-12936d27b7b8"
            name: "Prattville"
            updated_at: "2022-05-31T20:42:53.350872"
      404:
        description: No city found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def cities_delete(city_id):
    """
    Delete a City object
    ---
    tags:
      - City
    parameters:
      - name: city_id
        in: path
        required: true
    responses:
      200:
        description: City deleted
        schema:
          type: object
      404:
        description: No city found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def new_city(state_id):
    """
    Creates a new City
    ---
    tags:
      - City
    parameters:
      - name: create_city
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
          example:
            name: "Rome"
    responses:
      201:
        description: City created
        schema:
          type: object
          properties:
            __class__:
              type: string
            created_at:
              type: string
            id:
              type: string
            name:
              type: string
            updated_at:
              type: string
          example:
            __class__: "City"
            created_at: "2022-05-31T20:42:53.350872"
            id: "6149e15b-90a4-4d42-9d00-8342774d18b6"
            name: "Rome"
            updated_at: "2022-05-31T20:42:53.350872"
      400:
        description: User error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing name"
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    new_city = request.get_json()
    if not new_city:
        abort(400, 'Not a JSON')
    if 'name' not in new_city:
        abort(400, 'Missing name')
    new_city['state_id'] = state_id
    city = City(**new_city)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_id_put(city_id):
    """
    Updates a City object
    ---
    tags:
      - City
    parameters:
      - name: city_id
        in: path
        required: true
      - name: update_city
        description: City's information to be updated
        in: body
        required: true
        example:
          {
            "name": "Akron"
          }
    responses:
      200:
        description: City updated
        schema:
          type: object
          properties:
            __class__:
              type: string
            created_at:
              type: string
            id:
              type: string
            name:
              type: string
            updated_at:
              type: string
          example:
            __class__: "City"
            created_at: "2022-05-31T20:42:53.350872"
            id: "547e94f1-ff98-4cbb-b2e6-c1878f9464a7"
            name: "Akron"
            updated_at: "2022-05-31T20:42:53.350872"
      400:
        description: Invalid JSON
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not a JSON"
      404:
        description: No city found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_json = request.get_json()
    if not request_json:
        abort(400, 'Not a JSON')
    for key, value in request_json.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
