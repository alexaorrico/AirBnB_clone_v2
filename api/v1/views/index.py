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
    for this_class in storage.classes().values():
        ret_dict[this_class.__name__] = storage.count(this_class)
    return jsonify(ret_dict)
