#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def json_string():
    new = {}
    new['status'] = "OK"
    return jsonify(new)


@app_views.route('/stats')
def obj_by_count():
    new = {}
    cls_dict = {'amenities': Amenity, 'cities': City, 'places': Place,
                'reviews': Review, 'states': State, 'users': User}

    for key, val in cls_dict.items():
        new[key] = storage.count(val)

    return jsonify(new)
