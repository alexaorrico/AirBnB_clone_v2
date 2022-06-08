#!/usr/bin/python3
"""amenities api"""

from api.v1.views import app_views
from models.engine.db_storage import classes
from models import storage
from flask import jsonify, abort, request

@app_views.route("/amenities", methods=["GET", "POST"])
@app_views.route("/amenities/<amenity_id>", methods=["GET", "PUT", "DELETE"])
def amenities_view(amenity_id=None):
    if amenity_id:
        amenity_obj = storage.get(classes["Amenity"], amenity_id)
        if not amenity_obj:
            abort(404)

        if request.method == "GET":
            amenity_obj = amenity_obj.to_dict()
                
            return jsonify(amenity_obj)
        elif request.method == "PUT":
            try:
                obj_json = request.get_json()
            except:
                return jsonify({"error": "Not found"}), 400

            for key, value in obj_json.items():
                if key not in ["updated_at", "id", "created_at"]:
                    setattr(amenity_obj, key, value)

            amenity_obj.save()

            amenity_obj = amenity_obj.to_dict()
            return jsonify(amenity_obj), 200
        elif request.method == "DELETE":
            amenity_obj.delete()
            storage.save()

            return jsonify({})
    else:
        if request.method == "GET":
            amenity_list = []
            amenities = storage.all(classes["Amenity"])
            for k, v in amenities.items():
                amenity_list.append(v.to_dict())
            return jsonify(amenity_list)

        else:
            # falsee = request.is_json()
            # if  not falsee:
            #     return jsonify({"error": "Not a JSON"}), 400

            obj_json = request.get_json()

            if "name" not in obj_json.keys():
                return jsonify({"error": "Missing name"}), 400

            new_amenity = classes["Amenity"](name = obj_json["name"])
            new_amenity.save()

            new_amenity_dict = new_amenity.to_dict()
            return jsonify(new_amenity_dict), 201
