#!/usr/bin/python3
"""view states object"""


from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify


@app_views.route('/states')
def states():
    """return list of all objects State"""
    new_list = list()
    for value in storage.all('State').values():
        new_list.append(value.to_dict())
    return new_list


