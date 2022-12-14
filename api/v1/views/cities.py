#!/usr/bin/python3
""" State endpoints """
from flask import jsonify, request, abort
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<string:state_id>/cities', methods=["GET", "POST"])
def cities_by_state(state_id):
    """Retrieves all cities of a State object or add a new City by state_id"""
    # hay codigo repetido, se puede optimizar

    if request.method == 'GET':
        detector = 0
        for obj in storage.all("State").values():
            if obj.id == state_id:
                detector = 1
                break
            else:
                pass

        if detector != 0:
            results = []
            for city in storage.all("City").values():
                if city.state_id == state_id:
                    results.append(city.to_dict())
            return jsonify(results)
        else:
            abort(404)

    elif request.method == 'POST':
        detector = 0
        for obj in storage.all("State").values():
            if obj.id == state_id:
                detector = 1
                break
            else:
                pass

        if detector != 0:
            http_data = request.get_json()
            if not http_data:
                abort(400, 'Not a JSON')
            if "name" not in http_data:
                abort(400, 'Missing name')

            http_data["state_id"] = state_id
            new_city = City(**http_data)
            new_city.save()
            return jsonify(new_city.to_dict()), 201
        else:
            abort(404)


@app_views.route('/cities/<string:city_id>', methods=["GET", "DELETE", "PUT"])
def city_by_id(city_id):
    """Retrieves, deletes or updates a City object by city_id"""
    # tambien se puede optimizar, manito

    if request.method == 'GET':
        for obj in storage.all("City").values():
            if obj.id == city_id:
                return jsonify(obj.to_dict())

    elif request.method == 'DELETE':
        for obj in storage.all("City").values():
            if obj.id == city_id:
                storage.delete(obj)
                storage.save()
                return jsonify({}), 200

    elif request.method == 'PUT':
        for obj in storage.all("City").values():
            if obj.id == city_id:
                http_data = request.get_json()
                if not http_data:
                    abort(400, 'Not a JSON')

                statics_attrs = ["id", "created_at", "updated_at"]
                for key, value in http_data.items():
                    if key not in statics_attrs:
                        setattr(obj, key, value)
                storage.save()
                return jsonify(obj.to_dict()), 200

    abort(404)
