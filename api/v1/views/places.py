#!/usr/bin/python3
"""places api"""

from api.v1.views import app_views
from models.engine.db_storage import classes
from models import storage
from flask import jsonify, abort, request

@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"])
@app_views.route("/places/<place_id>", methods=["GET", "PUT", "DELETE"])
def places_view(city_id=None, place_id=None):
    if city_id:
        city_obj = storage.get(classes["Amenity"], city_id)
        if not city_obj:
            abort(404)

        if request.method == "GET":
            places_list = []
            for place in city_obj.places:
                place_dict = place.to_dict()
                places_list.append(place_dict)
                
            return jsonify(places_list)
        else:
            request_dict = request.get_json()
            if "name" not in request_dict.keys():
                return jsonify({"error": "Missing name"}), 400

            if "user_id" not in request_dict.keys():
                return jsonify({"error": "Missing user_id"}), 400

            if not storage.get(request_dict.get("user_id")):
                abort(404)
            
            new_place = classes["Place"](name = request_dict["name"], 
                                        city_id = city_id,
                                        user_id = request_dict["user_id"],
                                        description = request_dict.get("description"),
                                        number_rooms = request_dict.get("number_rooms"),
                                        number_bathrooms = request_dict.get("number_bathrooms"),
                                        max_guest = request_dict.get("max_guest"),
                                        price_by_night = request_dict.get("price_by_night"),
                                        latitude = request_dict.get("latitude"),
                                        longitude = request_dict.get("longitude")
                                        )
            new_place.save()

            new_place_dict = new_place.to_dict()
            return jsonify(new_place_dict), 201
    else:
        place_obj = storage.get(classes["Place"], place_id)
        if not place_obj:
            abort(404)

        if request.method == "GET":
            place_obj = place_obj.to_dict()
                
            return jsonify(place_obj)
        elif request.method == "PUT":
            try:
                obj_json = request.get_json()
            except:
                return jsonify({"error": "Not found"}), 400

            for key, value in obj_json.items():
                if key not in ["updated_at", "id", "created_at", "user_id", "city_id"]:
                    setattr(place_obj, key, value)

            place_obj.save()

            place_obj = place_obj.to_dict()
            return jsonify(place_obj), 200
        elif request.method == "DELETE":
            place_obj.delete()
            storage.save()

            return jsonify({})
