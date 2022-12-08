#!/usr/bin/python3
""" State endpoints """
from flask import jsonify, request, abort
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<string:state_id>/cities', methods=["GET"])
def cities_by_state(state_id):
    """Retrieves all cities of a State object by state_id"""
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
