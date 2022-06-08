#!/usr/bin/python3
"""cities api"""


from api.v1.views import app_views
from models.engine.db_storage import classes
from models import storage
from flask import abort, jsonify, request

@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
@app_views.route("/cities/<city_id>", methods=["GET", "PUT", "DELETE"])
def cities_views(state_id=None, city_id=None):
    if state_id:
        state_obj = storage.get(classes["State"], state_id)
        if not state_obj:
            abort(404)

        if request.method == "GET":
            cities_list = []
            for city in state_obj.cities:
                city_dict = city.to_dict()
                cities_list.append(city_dict)
                
            return jsonify(cities_list)
        else:
            request_dict = request.get_json()
            if "name" not in request_dict.keys():
                return jsonify({"error": "Missing name"}), 400
            
            new_city = classes["City"](name = request_dict["name"], state_id = state_id)
            new_city.save()

            new_city_dict = new_city.to_dict()
            return jsonify(new_city_dict), 201

    else:
        city_obj = storage.get(classes["City"], city_id)
        if not city_obj:
            abort(404)

        if request.method == "GET":
            city_dict = city_obj.to_dict()
            return jsonify(city_dict)

        elif request.method == "PUT":
            try:
                obj_json = request.get_json()
            except:
                return jsonify({"error": "Not found"}), 400

            for key, value in obj_json.items():
                if key not in ["updated_at", "id", "created_at"]:
                    setattr(city_obj, key, value)

            city_obj.save()

            city_obj = city_obj.to_dict()
            return jsonify(city_obj), 200

        else:
            city_obj.delete()
            storage.save()

            return jsonify({})
