#!/usr/bin/python3
"""Status of your API"""

from api.v1.views.index import *
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)

_host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
_port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else 5000

app.register_blueprint(app_views, url_prefix="/api/v1")

@app.teardown_appcontext
def cleanup(exception):
    storage.close()

@app.errorhandler(404)
def error_404(exception):
    return jsonify(error="Not found"), 404
    
    
if __name__ == "__main__":
    app.run(host=_host, port=_port, threaded=True, debug=True)
