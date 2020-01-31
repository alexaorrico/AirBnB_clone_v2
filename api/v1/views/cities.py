#!/usr/bin/python3
"""
    ~~state~~ city endpoint
"""
from flask import request, jsonify
from api.v1.views import app_views
from models.city import City
from api.v1.views.general import do
from models import storage


@app_views.route("/states/<id>/cities", methods=["GET", "POST"])
def states_id_cities(id):
    """ list or create """
    city = [c for c in storage.all("State").values() if c.id == id]
    if not city:
        return {"error": "Not found"}, 404
    
    if request.method == "GET":
        return (jsonify([
            s.to_dict() for s
            in storage.all("City").values()
            if s.state_id == id
        ]), 200)
    elif request.method == "POST":
        try:
            data = request.get_json()
            if "name" not in data:
                return {"error": "Not found"}, 404
        except:
            return {"error": "Not found"}, 404
        # make sure state id is valid
        found = False
        for state in storage.all("State").values():
            if state.id == id:
                found = True
                break
        if not found:
            return {"error": "Not found"}, 404

        new = City()
        for key in data:
            setattr(new, key, data[key])
        setattr(new, "state_id", id)
        new.save()
        return new.to_dict(), 201
    return {"error": "Not found"}, 404


@app_views.route("/cities/<id>", methods=["GET", "PUT", "DELETE"])
def cities_id(id):
    """ states """
    return do(City, id)
