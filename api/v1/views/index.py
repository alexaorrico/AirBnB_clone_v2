#!/usr/bin/python3
""" API redirections """


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ returns status OK if app is working """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ return object count for each class """
    ret_dict = {}
    display_name_dict = {"Amenity": "amenities",
                         "City": "cities",
                         "Place": "places",
                         "Review": "reviews",
                         "State": "states",
                         "User": "users"}

    for this_class in storage.classes().values():
        if this_class.__name__ in display_name_dict.keys():
            display_name = display_name_dict.get(this_class.__name__)
        else:
            display_name = this_class.__name__
        ret_dict[display_name] = storage.count(this_class)
    return jsonify(ret_dict)
