#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from api.vi.views import app_views


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_places():
    """Retreive the list of all places objects"""
    places = storage.all(Place).values()
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slasheds=False)
def get_place(place_id):
    """Retrieve the specific place object by Id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slasheds=False)
def delete_place(place_id):
    """Delete a Place object by ID"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places', methods=['POST'], strict_slasheds=False)
def create_place():
    """Create a new place object"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slasheds=False)
def update_place(place_id):
    """Update a Place Object by ID"""
    if place:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a Json"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(place, key, value)


        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
