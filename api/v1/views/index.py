#!/usr/bin/pyton3
""" Index.py: return json content"""

from api.v1.views import app_views

@app_views.route("/status")
def status_ch(self):
    """ Checking status code """
    return jsonify({"status": "OK"}) 
