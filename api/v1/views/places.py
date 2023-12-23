#!/usr/bin/python3
"""new view for Place objects that handles all default RESTFul API actions"""
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


@app_views.route('/places', methods=['GET'])
def all_places():
    all_places = []
    for place in storage.all(Place).values():
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def Place_obj(place_id):
    if storage.get(Place, place_id) is None:
        abort(404)
    return jsonify(storage.get(Place, place_id).to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_Place(place_id):
    if storage.get(Place, place_id) is None:
        abort(404)
    storage.delete(storage.get(Place, place_id))
    storage.save()
    return {}, 200


@app_views.route('/places/', methods=['POST'])
def create_Place():
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_Place(place_id):

    existing_place = storage.get(Place, place_id)
    if existing_place is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for k, v in data.items():
        if k not in {'id', 'created_at', 'updated_at'}:
            setattr(existing_place, k, v)
    storage.save()
    return jsonify(existing_place.to_dict()), 200
