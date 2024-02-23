#!/usr/bin/python3
'''Module containing instructions for the flask blueprint app_views'''
from api.v1.views import app_views
from api import mapped_classes
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def all_places(city_id):
    '''Retrieves all Places objects associated with city_id'''
    content = storage.get("City", city_id)
    if content is None:
        abort(404)
    else:
        info = content.places
        rqd_info = []
        for item in info:
            rqd_info.append(item.to_dict())
        return jsonify(rqd_info)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def post_make_new_place(city_id):
    '''Create a Place object with the values provided'''
    json_content = request.get_json()
    if not json_content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in json_content:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if json_content is None:
        abort(404)
    content = storage.get("City", city_id)
    if content is None:
        abort(404)
    if not content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    usr_obj = storage.get("User", content["user_id"])
    if usr_obj is None:
        abort(404)
    if "name" not in usr_obj:
        return make_response(jsonify({"error": "Missing name"}), 400)
    json_content["city_id"] = city_id
    new_place = mapped_classes["Place"](**json_content)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_specific_place(place_id):
    '''Get a specific place by the id given'''
    content = storage.get("Place", place_id)
    if content is None:
        abort(404)
    else:
        return jsonify(content.to_dict())


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_spcific_place(place_id):
    '''Delete a specific place else raise an error'''
    content = storage.get("Place", place_id)
    if content is None:
        abort(404)
    else:
        storage.delete(content)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_specified_place(place_id):
    '''Update a sepcific place as specified by ID'''
    content = storage.get("Place", place_id)
    if content is None:
        abort(404)
    else:
        update_dict = request.get_json()
        if not update_dict:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        update_dict.pop("id", None)
        update_dict.pop("created_at", None)
        update_dict.pop("updated_at", None)
        update_dict.pop("city_id", None)
        update_dict.pop("user_id", None)
        for key, value in update_dict.items():
            setattr(content, key, value)
        content.save()
        return jsonify(content.to_dict()), 200
