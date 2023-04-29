#!/usr/bin/python3
""" starts a Flask web application """
from api.v1.views import app_views

@app_views.route('/status')
def status():
    return { "status": "OK" }
