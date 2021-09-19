#!/usr/bin/python3
""" Index Module"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def number_by_objects():
    """"""
    objs = storage.all()
    classes = []
    names = []
    dict = {}
    for obj, value in objs.items():
        cls = value.__class__.__name__
        if cls not in classes:
            classes.append(cls)
            letter = cls[-1:]
            if letter != 'y':
                name = cls[:].lower() + "s"
                names.append(name)
            else:
                name = cls[0:-1].lower() + "ies"
                names.append(name)

    print("{}".format(names))
    for i in range(len(classes)):
        dict[names[i]] = storage.count(classes[i])
    return jsonify(dict)
