from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by(state_id):
    state = storage.get(State, state_id)
    city_dict = []
    for city in state.cities:
            city_dict.append(city.to_dict())
    return jsonify(city_dict)

@app_views.route('/cities/<string:city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    try:
        city = storage.get(City, city_id)
        return jsonify(city.to_dict())
    except KeyError:
        abort(404)

@app_views.route('/cities/<string:city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    try:
        city = storage.get(City, city_id)
        city.delete()
        storage.save()
        return jsonify({})
    except KeyError:
        abort(404)

@app_views.route('/states/<string:state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    try:
        state = storage.get(State, state_id)
        data = request.get_json()
        if data.get("name") is None:
            return make_response(jsonify({"error" : "Missing name"}), 400)
        data["state_id"] = state_id
        city = City(**data)
        city.save()
        response = jsonify(city.to_dict())
        return make_response(response, 201)
    except KeyError:
        abort(404)
    except Exception:
        return make_response(jsonify({"error" : "Not a JSON"}), 400)


@app_views.route('/cities/<string:city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    try:
        data = request.get_json()
        city = storage.get(City, city_id)
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict())
    except KeyError:
        abort(404)
    except Exception:
        return make_response(jsonify({"error" : "Not a JSON"}), 400)
