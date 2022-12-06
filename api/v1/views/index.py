#!/usr/bin/python3
"""Index"""


from api.v1.views import app_views
import json


@app_views.route('/status')
def status():
    return {"status": "ok"}
