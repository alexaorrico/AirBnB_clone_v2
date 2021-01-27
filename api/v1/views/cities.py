#!/usr/bin/python3
"""this is a test string"""

from flask import request, abort, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<s_id>/cities",
                 strict_slashes=False,
                 methods=["GET", "POST"])
def cities_base(s_id):
    """this is a test string"""
    if request.method == "GET":
        out = []
        for state in storage.all("State").values():
            if state.id == s_id:
                for city in state.cities:
                    out.append(city.to_dict())
                return jsonify(out)
        abort(404)
    if request.method == "POST":
        if not request.is_json:
            return "Not a JSON", 400
        for state in storage.all("State").values():
            if state.id == s_id:
                kwargs = {"state_id": s_id}
                kwargs.update(request.get_json())
                out = City(**kwargs)
                if "name" not in out.to_dict().keys():
                    return "Missing name", 400
                out.save()
                return out.to_dict(), 201
        abort(404)


@app_views.route("/cities/<c_id>",
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def cities_id(c_id):
    """this is a test string"""
    if request.method == "GET":
        for city in storage.all("City").values():
            if city.id == c_id:
                return city.to_dict()
        abort(404)
    if request.method == "DELETE":
        for city in storage.all("City").values():
            if city.id == c_id:
                city.delete()
                storage.save()
                return {}, 200
        abort(404)
    if request.method == "PUT":
        for city in storage.all("City").values():
            if city.id == c_id:
                if not request.is_json:
                    return "Not a JSON", 400
                for k, v in request.get_json().items():
                    if k not in ["id", "state_id", "created_at", "updated_at"]:
                        setattr(city, k, v)
                storage.save()
                return city.to_dict(), 200
        abort(404)
