#!/usr/bin/python3
'''creates a new view for place objects'''
from models import storage
from api.v1.views import app_views
from models.places import Place
from flask import jsonify, request, abort


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def getter_places():
    '''getter_places - gets all Place objects'''
    new_list = []
    allplaces = list(storage.all("Place").values())

    for place in allplaces:
        new_list.append(place.to_dict())
    return jsonify(new_list)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def getter_places_id(place_id):
    '''getter_id - gets all Place objects by id'''
    try:
        place = storage.get(Place, place_id).to_dict()
        return jsonify(place)
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def deleter_places(place_id):
    '''deleter_id - delete an object by id'''
    id = storage.get(Place, place_id)

    if id is not None:
        storage.delete(id)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/places/', methods=['POST'], strict_slashes=False)
def post_place():
    '''post_place - create an place object with post'''
    try:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        body_dict = request.get_json()
        if "name" not in body_dict:
            return jsonify({"error": "Missing name"}), 400
        place = Place(name=body_dict["name"])
        place.save()
        return jsonify(place.to_dict()), 201
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    '''put_place - updates a place object by id'''
    placeId = storage.get(Place, place_id)

    if placeId is None:
        abort(404)
    body_dict = request.get_json()
    if body_dict is None:
        abort(400, "Not a JSON")
    body_dict.pop("id", None)
    body_dict.pop("created_at", None)
    body_dict.pop("updated_at", None)
    for key, value in body_dict.items():
        setattr(placeId, key, value)
    placeId.save()
    return jsonify(placeId.to_dict()), 200
