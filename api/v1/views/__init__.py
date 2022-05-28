#!/usr/bin/python3
""""""
from flask import Blueprint

print("heeerrre", __name__)
app_views = Blueprint('/api/v1', __name__)
# La intranet dice que PEP 8 se va a quejar por el orden de la importación 
# pero que este módulo no se va a checkear

"""@app_views.route('/status', strict_slashes=False)
def status():
    return "jsonify({'status': 'OK'})"""

from api.v1.views import *
from api.v1.views import index
