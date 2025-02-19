#!/usr/bin/python3
"""City for RESTFul API"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def state_id(state_id=None):
    """Cities
    ---
    tags:
        - City
    parameters:
      - name:  state_id
        in: path
        type: string
    responses:
      200:
        description: List of states
      404:
        description: Resource not found
      400:
        description: Not a JSON
    """
    list_cities = []
    state_obj = storage.get('State', str(state_id))
    if state_obj is None:
        abort(404)
    else:
        for city_obj in storage.all("City").values():
            if city_obj.state_id == str(state_id):
                list_cities.append(city_obj.to_dict())
        return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=["GET"])
def cities(city_id=None):
    """Cities
    ---
    tags:
        - City
    parameters:
      - name: city_id
        in: path
        type: string
    responses:
      200:
        description: List of states
      404:
        description: Resource not found
      400:
        description: Not a JSON
    """
    state_objs = storage.get("City", city_id)
    if not state_objs:
        abort(404)
    else:
        return jsonify(state_objs.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def cities_delete(city_id=None):
    """Cities
    ---
    tags:
        - City
    parameters:
      - name: city_id
        in: path
        type: string
    responses:
      200:
        description: List of states
      404:
        description: Resource not found
      400:
        description: Not a JSON
    """
    obj_city = storage.get('City', city_id)
    if obj_city is None:
        abort(404)
    obj_city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'])
def city_put(city_id):
    """Cities
    ---
    tags:
        - City
    parameters:
      - name: city_id
        in: path
        type: string
    responses:
      200:
        description: List of states
      404:
        description: Resource not found
      400:
        description: Not a JSON
    """
    obj_city = storage.get('City', city_id)
    if obj_city is None:
        abort(404)
    do_put = request.get_json()
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in do_put.items():
        if k is not "id" and k is not "created_at":
            if k is not "updated_at" and k is not "state_id":
                setattr(obj_city, k, v)
    obj_city.save()
    return jsonify(obj_city.to_dict()), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def city_post(state_id):
    """Create city
     ---
     tags:
         - City
     parameters:
         - name: state_id
           in: path
           type: string
         - name: name
           in: body
           type: dictionary
     responses:
       200:
         description: New state
       400:
         description: Not a JSON
       400:
         description: Missind name
    """
    obj_state = storage.get("State", state_id)
    if obj_state is None:
        abort(404)
    if request.json:
        if "name" in request.json:
            do_post = request.get_json()
            do_post["state_id"] = str(state_id)
            new_obj = City(**do_post)
            new_obj.save()
            return jsonify(new_obj.to_dict()), 201
        else:
            return jsonify({"error": "Missing name"}), 400
    else:
        return jsonify({"error": "Not a JSON"}), 400
