from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<string:city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by(city_id):
    city = storage.get(City, city_id)
    place_dict = []
    for place in city.places:
            place_dict.append(place.to_dict())
    return jsonify(place_dict)

@app_views.route('/places/<string:place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    try:
        place = storage.get(Place, place_id)
        return jsonify(place.to_dict())
    except KeyError:
        abort(404)

@app_views.route('/places/<string:place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    try:
        place = storage.get(Place, place_id)
        place.delete()
        storage.save()
        return jsonify({})
    except KeyError:
        abort(404)

@app_views.route('/cities/<string:city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    try:
        city = storage.get(City, city_id)
        data = request.get_json()
        if data.get("name") is None:
            return make_response(jsonify({"error" : "Missing name"}), 400)
        if data.get("user_id") is None:
            return make_response(jsonify({"error" : "Missing user_id"}), 400)
        data["city_id"] = city_id
        place = Place(**data)
        place.save()
        response = jsonify(place.to_dict())
        return make_response(response, 201)
    except KeyError:
        abort(404)
    except Exception:
        return make_response(jsonify({"error" : "Not a JSON"}), 400)


@app_views.route('/places/<string:place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    try:
        data = request.get_json()
        place = storage.get(Place, place_id)
        for key, value in data.items():
            if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                continue
            setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict())
    except KeyError:
        abort(404)
    except Exception:
        return make_response(jsonify({"error" : "Not a JSON"}), 400)
