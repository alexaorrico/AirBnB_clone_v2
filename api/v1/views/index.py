#!/usr/bin/python3
''' creates a route giving the status '''
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


@app_views.route('/status', methods=['GET'])
def json_string():
    ''' returns a JSON rep of the status of flask '''
    new = {}
    new['status'] = "OK"
    return jsonify(new)


@app_views.route('/stats', methods=['GET'])
def obj_by_count():
    ''' retrieves the number of each objects by type '''
    new = {}
    cls_dict = {'amenities': Amenity, 'cities': City, 'places': Place,
                'reviews': Review, 'states': State, 'users': User}

    for key, val in cls_dict.items():
        new[key] = storage.count(val)

    return jsonify(new)
