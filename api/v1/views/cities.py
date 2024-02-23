#!/usr/bin/python3
'''Module containing instructions for the flask blueprint app_views'''
from api.v1.views import app_views
from api import mapped_classes
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def all_cities(state_id):
    '''Retrieves all City objects associated with state_id'''
    content = storage.get("State", state_id)
    if content is None:
        abort(404)
    else:
        info = content.cities
        rqd_info = []
        for item in info:
            rqd_info.append(item.to_dict())
        return jsonify(rqd_info)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def post_make_new_city(state_id):
    '''Create a City object is with the values provided'''
    json_content = request.get_json()
    if not json_content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in json_content:
        return make_response(jsonify({"error": "Missing name"}), 400)
    content = storage.get("State", state_id)
    if content is None:
        abort(404)
    json_content["state_id"] = state_id
    new_city = mapped_classes["City"](**json_content)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def specific_city(city_id):
    '''Get a specific city by the id given'''
    content = storage.get("City", city_id)
    if content is None:
        abort(404)
    else:
        return jsonify(content.to_dict())


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_spcific_city(city_id):
    '''Delete a specific city else raise an error'''
    content = storage.get("City", city_id)
    if content is None:
        abort(404)
    else:
        storage.delete(content)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_specified_city(city_id):
    '''Update a sepcific city as identified by ID'''
    content = storage.get("City", city_id)
    if content is None:
        abort(404)
    else:
        update_dict = request.get_json()
        if not update_dict:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        update_dict.pop("id", None)
        update_dict.pop("created_at", None)
        update_dict.pop("updated_at", None)
        update_dict.pop("state_id", None)
        for key, value in update_dict.items():
            setattr(content, key, value)
        content.save()
        return jsonify(content.to_dict()), 200
