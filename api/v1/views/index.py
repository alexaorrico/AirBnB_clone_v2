#!/usr/bin/python3
"""
set up route for status endpoint
"""


from api.v1.views import app_views


@app_views.route('/status')
def get_status():
    """ send status api"""
    return {"status": "OK"}
