#!/usr/bin/python3
"""Places view module"""

from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


app = Flask(__name__)


def get_city(city_id):
    city = City.query.get(city_id)
    if city is None:
        abort(404, description="City not found")
    return city


def get_place(place_id):
    place = Place.query.get(place_id)
    if place is None:
        abort(404, description="Place not found")
    return place


def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404, description="User not found")
    return user


@app.route('/api/v1/cities/<int:city_id>/places', methods=['GET'])
def get_places(city_id):
    city = get_city(city_id)
    places = Place.query.filter_by(city_id=city_id).all()
    return jsonify([place.to_dict() for place in places])


@app.route('/api/v1/places/<int:place_id>', methods=['GET'])
def get_place_detail(place_id):
    place = get_place(place_id)
    return jsonify(place.to_dict())


@app.route('/api/v1/places/<int:place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = get_place(place_id)
    place.delete()
    return jsonify({}), 200


@app.route('/api/v1/cities/<int:city_id>/places', methods=['POST'])
def create_place(city_id):
    city = get_city(city_id)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if 'user_id' not in data:
        abort(400, description="Missing user_id")

    user = get_user(data['user_id'])

    if 'name' not in data:
        abort(400, description="Missing name")

    new_place = Place(name=data['name'], user_id=user.id, city_id=city.id)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app.route('/api/v1/places/<int:place_id>', methods=['PUT'])
def update_place(place_id):
    place = get_place(place_id)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    # Update the Place object with all key-value pairs of the dictionary
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200