#!/usr/bin/python3
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ return ok """
    return {"status": "OK"}
