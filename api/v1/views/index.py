
'''contains blueprint for making app components'''
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    '''route that returns a JSON status'''
    return(jsonify({"status": "OK"}))