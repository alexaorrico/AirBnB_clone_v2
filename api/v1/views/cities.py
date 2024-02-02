#!/usr/bin/python3
"""
handles all default RestFul API actions for cities
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views, City, storage


@app_views.route('/states/<int:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def view_all_cities(state_id=None):
    """
    Retrieves a list of all the cities
    ---
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
            items:
              $ref: '#/definitions/Color'

      Color:
        type: string
    responses:
        200:
            description: A list of dictionarys, each dict is a City
            schema:
            $ref: '#/definitions/City'
            examples:
                [{'__class__': 'City', 'created_at': '2017-03-25T02:17:06',
                'id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f', 'name': 'Portland',
                'state_id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f',
                'updated_at': '2017-03-25T02:17:06'}]

    """
    body = storage.get("State", state_id)
    if body is None:
        abort(404)
    cities = []
    for city in body.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<int:cities_id>',
                 methods=['GET'], strict_slashes=False)
def view_city(cities_id=None):
    """
    Retrieves a city by a given id
    ---
    parameters:
      - name: cities_id
        in: path
        type: string
        enum: ['None', '10098698-bace-4bfb-8c0a-6bae0f7f5b8f']
    responses:
      200:
        description: A dictionary of a City
        schema:
          $ref: '#/definitions/City'
        examples:
            {'__class__': 'City', 'created_at': '2017-03-25T02:17:06',
            'id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f', 'name': 'Portland',
            'state_id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f',
            'updated_at': '2017-03-25T02:17:06'}
    """
    body = storage.get("City", cities_id)
    if body is None:
        abort(404)
    return jsonify(body.to_dict())


@app_views.route('/cities/<int:city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    """
    Deletes a city by a given id
    ---
    parameters:
      - name: city_id
        in: path
        type: string
        enum: ['None', '10098698-bace-4bfb-8c0a-6bae0f7f5b8f']
    responses:
      200:
        description: An empty dictionary
        schema:
          $ref: '#/definitions/City'
        examples:
            {}
    """
    body = storage.get("City", city_id)
    if body is None:
        abort(404)
    storage.delete(body)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<int:state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id=None):
    """
    Creates a city
    ---
    parameters:
      - name: state_id
        in: path
        type: string
        enum: ['None', '10098698-bace-4bfb-8c0a-6bae0f7f5b8f']
    responses:
      200:
        description: A dictionary of a City
        schema:
          $ref: '#/definitions/City'
        examples:
            {'__class__': 'City', 'created_at': '2017-03-25T02:17:06',
            'id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f', 'name': 'Portland',
            'state_id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f',
            'updated_at': '2017-03-25T02:17:06'}
    """
    body = None
    try:
        body = storage.get("State", state_id)
    except:
        body = None
    if body is None:
        abort(404)
    try:
        content = request.get_json()
    except BaseException:
        content = None
    if content is None:
        abort(400, "Not a JSON")
    if 'name' not in content.keys():
        abort(400, 'Missing name')
    content['state_id'] = state_id
    city = City(**content)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<int:city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """
    Updates a city
    ---
    parameters:
      - name: city_id
        in: path
        type: string
        enum: ['None', '10098698-bace-4bfb-8c0a-6bae0f7f5b8f']
    responses:
      200:
        description: A dictionary of a City
        schema:
          $ref: '#/definitions/City'
        examples:
            {'__class__': 'City', 'created_at': '2017-03-25T02:17:06',
            'id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f', 'name': 'Portland',
            'state_id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f',
            'updated_at': '2017-03-25T02:17:06'}
    """
    body = None
    try:
        body = storage.get("City", city_id)
    except:
        body = None
    if body is None:
        abort(404)
    try:
        content = request.get_json()
    except:
        content = None
    if content is None:
        abort(400, "Not a JSON")
    for key, value in content.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(body, key, value)
    body.save()
    return jsonify(body.to_dict()), 200
