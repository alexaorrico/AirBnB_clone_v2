#!/usr/bin/python3
"""restful API functions for Amenity"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import request, jsonify, abort


@app_views.route("/amenities",
                 strict_slashes=False,
                 methods=["GET", "POST"]
                 )
@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["DELETE", "PUT", "GET"])
def amenity_end_points(amenity_id=None):
    """to get amenities"""
    obj_amenities = storage.all(Amenity)
    my_dict = [obj.to_dict() for obj in obj_amenities.values()]
    if not amenity_id:
        if request.method == "GET":
            return jsonify(my_dict)

        elif request.method == "POST":
            imput = request.get_json()
            if not imput:
                abort(400, "Not a JSON")
            elif not imput["name"]:
                abort(400, "Missing name")
            else:
                new_amenity = Amenity(**imput)
                new_amenity.save()
                return jsonify(new_amenity.to_dict()), 201
    else:
        if request.method == "GET":
            for amenity in my_dict:
                if amenity.get('id') == amenity_id:
                    return jsonify(amenity)
            abort(404)
        elif request.method == "DELETE":
            for ob in obj_amenities.values():
                if ob.id == amenity_id:
                    storage.delete(ob)
                    storage.save()
                    return jsonify({}), 200
            abort(404)
        elif request.method == "PUT":
            new_dict = storage.get("Amenity", amenity_id)
            get_new_name = request.get_json()
            if not get_new_name:
                abort(400, "Not a JSON")
            for amenity in obj_amenities.values():
                if amenity.id == amenity_id:
                    new_dict.name = get_new_name.get("name")
                    new_dict.save()
                    return jsonify(new_dict.to_dict()), 200
            abort(404)
