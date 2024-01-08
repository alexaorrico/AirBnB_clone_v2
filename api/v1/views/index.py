#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
from flask import jsonify
#from models import storage


@app_views.route('/status')
def status():
    """ Returns JSON """
    return jsonify(status="OK")
