#!/usr/bin/python3

from api.v1.views import app_views
from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)
app.register_blueprint(app_views)

@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def citybystate(state_id):
    """"""
    ctz = []
    all = storage.get(State, state_id)
    if all is not None:
        cties = all.cities
        for city in cties:
            data = storage.get(City, city.id)
            ctz.append(data.to_dict())
        return jsonify(ctz)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrieve_all(city_id):
    """"""
    all = storage.get(City, city_id)
    if all is not None:
        return jsonify(all.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deletebyid(city_id):
    """deletebyid"""
    all = storage.get(City, city_id)
    if all is not None:
        storage.delete(all)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def postcitybyid(state_id):
    """"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    all = storage.get(State, state_id)
    if all is None:
        abort(404)
    if "name" not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    else:
        data = request.get_json()
        data['state_id'] = state_id
        storage.new(data)
        storage.save()
        return jsonify(data.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'])
def putcity(city_id):
    """update ct"""

    all = storage.get(City, city_id)
    if all is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    all.name = data['name']
    all.save()
    return jsonify(all.to_dict())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
