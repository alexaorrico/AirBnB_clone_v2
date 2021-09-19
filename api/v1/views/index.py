#!/usr/bin/python3
""" Index Module"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def quantity():
    objs = storage.all()
    classes = []
    names = []
    dict = {}
    for obj, value in objs.items():
        cls = value.__class__.__name__
        if cls not in classes:
            classes.append(cls)
            letter = cls[-1:]
            if letter !=  'y':
                name = cls + "s"
                print("{}".format(name))
                names.append(name)
            else:
                name = letter + "ies"
                print("{}"[O].format(name))
                names.append(name)

    print("{}".format(names))
    for i in range(len(classes)):
        dict[names[i]] = storage.count('State')
    return jsonify(dict)
