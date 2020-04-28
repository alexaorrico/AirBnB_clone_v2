#!/usr/bin/python3

from models.base_model import *
from api.v1.views import app_views
from models import storage
from models.amenity import *
from flask import jsonify, abort, request, make_response
    

@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def amenities():
    ls = []
    amenities = storage.all('Amenity')
    if request.method == "GET":
        for key, value in amenities.items():
            ls.append(value.to_dict())
        return jsonify(ls)
    elif request.method == "POST":
        if not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        elif not 'name' in request.json:
            return make_response(jsonify({'error': "Missing name"}), 400)
        else:
            new = Amenity(**request.json)
            new.save()
            return make_response(new.to_dict(), 201)
           


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id):
    amenities = storage.all('Amenity')
    for key, value in amenities.items():
        if amenity_id == value.id:
            if request.method == "GET":
                return value.to_dict()
            elif request.method == "DELETE":
                storage.delete(value)
                storage.save()
                return {}
            elif request.method == "PUT":
                if not request.json:
                    return make_response(jsonify({'error': "Not a JSON"}), 400)
                else:
                    json = request.json
                    for key2, value2 in json.items():
                        if key2 != 'id' and key2 != 'created_at' and key2 != "updated_at":
                            setattr(value, key2, value2)
                    value.updated_at = datetime.utcnow() 
                    storage.save()
                    return make_response(value.to_dict(), 200)
    abort(404)
