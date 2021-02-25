#!/usr/bin/python3
"""
create a new view for City objects that handles
all default RestFul API actions
"""

from flask import request, abort, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<s_id>/cities",
                 strict_slashes=False,
                 methods=["GET", "POST"])
def cities_base(s_id):
    """Retrieves the list of all City objects of a State"""
    if request.method == "GET":
        out = []
        state = storage.get(State, s_id)
        if state:
            for city in state.cities:
                out.append(city.to_dict())
            return jsonify(out)
        abort(404)
    if request.method == "POST":
        if not request.is_json:
            return "Not a JSON", 400
        state = storage.get(State, s_id)
        if state:
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
    """Retrieves a City object."""
    if request.method == "GET":
        city = storage.get(City, c_id)
        if city:
            return city.to_dict()
        abort(404)
    if request.method == "DELETE":
        city = storage.get(City, c_id)
        if city:
            city.delete()
            storage.save()
            return {}, 200
        abort(404)
    if request.method == "PUT":
        city = storage.get(City, c_id)
        if city:
            if not request.is_json:
                return "Not a JSON", 400
            for k, v in request.get_json().items():
                if k not in ["id", "state_id", "created_at", "updated_at"]:
                    setattr(city, k, v)
            storage.save()
            return city.to_dict(), 200
        abort(404)
