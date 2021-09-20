#!/usr/bin/python3

from api.v1.views import app_views
from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place


app = Flask(__name__)

@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def ret_all_bystate(city_id):
    """retrieve all by state"""
    places = []
    all = storage.get(City, city_id)
    if all is not None:
        plcs = all.places
        for x in plcs:
            ok = storage.get(Place, x.id)
            places.append(ok.to_dict())
        return jsonify(places)
    else:
        abort(404)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def ret_all(place_id):
    """retrieve all places"""
    all = storage.get(Place, place_id)
    if all is not None:
        return jsonify(all.to_dict())
    else:
        abort(404)


@app_views.route('places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_byid(place_id):
    """delete by place_id"""
    all = storage.get(Place, place_id)
    if all is not None:
        storage.delete(all)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_city(city_id):
    """postcity by city_id"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    all = storage.get(City, city_id)
    if all is None:
        abort(404)
    if "name" not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    if "user_id" not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", request.get_json()['user_id'])
    if user is None:
        abort(404)
    else:
        data = request.get_json()
        data['city_id'] = city_id
        ct = Place(**data)
        ct.save()
        return make_response(jsonify(ct.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'])
def put_city(place_id):
    """"""
    ignored = ['id', 'user_id', 'city_id', 'created_at',
               'updated_at']
    ct = storage.get(Place, place_id)
    if ct is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    for key, value in data.items():
        if key not in ignored:
            setattr(ct, key, value)
    ct.save()
    return jsonify(ct.to_dict())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
