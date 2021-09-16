#!/usr/bin/python3
""" Blueprint routes """
from api.v1.views import app_views

@app_views.route('/status')
def status():
    """ Return the status in JSON format """