from api.v1.views import app_views
import json
from flask import jsonify

@app_views.route("/status")
def check_status():
    """ return status ok as json"""
    dict_ = { 'status' : "ok"}
    
    return jsonify(dict_)