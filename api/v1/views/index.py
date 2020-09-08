#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json


@app_views.route('/status', methods=['GET'])
def retun_json():
    """ jsonify """
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'])
def number_cls_json():
    """ jsonify """

    list_bd = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    dict_list = {}
    var = {}
    for k, v in list_bd.items():
        result = storage.count(v)
        dict_list[k] = result
    return (dict_list)


if __name__ == "__main__":
    pass
