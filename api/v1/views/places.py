#!/usr/bin/python3
""" Place view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=[
                'GET', 'POST'])
def all_places(city_id=None):
    """ retrieves all Places """

    try:
        city = storage.all("City").pop("City." + city_id)
    except KeyError:
        abort(404)

    if request.method == "GET":
        my_places = [place.to_dict() for place in city.places]
        return (jsonify(my_places))

    if request.method == "POST":

        data = request.get_json(silent=True)
        if not data:
            return (jsonify({"error": "Not a JSON"}), 400)

        users = [user.id for user in storage.all("User").values()]

        if "user_id" not in data.keys():
            return (jsonify({"error": "Missing user_id"}), 400)
        if "name" not in data.keys():
            return (jsonify({"error": "Missing name"}), 400)
        if data.get("user_id") not in users:
            abort(404)
        place = Place(**data)
        place.city_id = city_id
        place.save()
        return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=[
                'GET', 'DELETE', 'PUT'])
def a_place(place_id):
    """ retrieves all Places """

    try:
        place = storage.all("Place").pop("Place." + place_id)
    except KeyError:
        abort(404)

    if request.method == 'GET':
        return (jsonify(place.to_dict()))

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return (jsonify({}), 200)

    data = request.get_json(silent=True)
    if not data:
        return (jsonify({"error": "Not a JSON"}), 400)

    if request.method == 'PUT':
        for k, v in data.items():
            if k not in [
                    'id', 'user_id', 'created_at', 'updated_at', 'city_id']:
                setattr(place, k, v)
        storage.new(place)
        storage.save()
        return (jsonify(place.to_dict()), 200)
